# Clearing Programming Interview Assignment: RSS Feed Parser in Python

Created: May 21, 2020 9:00 AM
Status: Ready to Start
URL: https://towardsdatascience.com/rss-feed-parser-in-python-553b1857055c

![1*S4iy1CDUP1npJcrKIXUb8g.jpeg](Clearing%20Programming%20Interview%20Assignment%20RSS%20Feed%20938e974d2de74cafa81c44cb68725b71/1S4iy1CDUP1npJcrKIXUb8g.jpeg)

# **Problem Elaboration**

So instead of diving right into the tech details, I’ll like to go over the problem context.
For those of you who don’t know, RSS is a web-based content (or feed) sharing format. ([https://en.wikipedia.org/wiki/RSS](https://en.wikipedia.org/wiki/RSS)).
Here are the details of the problem at hand:

1. A suitable data model to represent each posts needs to designed
2. Any relational database capable of python connectivity could be used to store the post data
3. Libraries capable of RSS parsing (such as feedparser) is forbidden
4. The load should be incremental, i.e., only records not processed earlier should get processed
5. The script should be scheduled to run once a day to get updates

Obviously I decided to use ***python 3.7***, with the end of life support coming for ***python 2.7***. **#3** above basically meant I had to implement the RSS parser on my own. All other decisions were pretty straight-forward given the time constraint of 1 day, leaving 3–4 hours for this work (assuming 8–9 hours given to the day job).
Here is what I ended up using:

> 1. The restriction of RSS parser libraries, basically expected me to write my own parser. Since it’s ultimately xml-based content, I decided to use the ever-reliable BeautifulSoup Library (https://www.crummy.com/software/BeautifulSoup/bs4/doc/)2. The relational database I chose was postgres (https://www.postgresql.org/). No particular reason, except ease of usage and familiarity and obviously an insanely popular open source support.3. Library apscheduler (https://apscheduler.readthedocs.io/en/latest/index.html) to schedule task once a day (a simple library to start with, airflow (https://airflow.apache.org/)/ azkaban (https://azkaban.github.io/) would’ve been an overkill)4. Library psycopg2 (https://pypi.org/project/psycopg2/) to support postgres (https://pypi.org/project/psycopg2/) (don’t think it needs an explanation, but didn’t want to use wrappers like SQLAlchemy (https://www.sqlalchemy.org/))5. Also, since no environment specifications were given, I decided to build all of this using two docker (https://www.docker.com/) containers, one for python and one for postgres.

With approach shared above, let’s get you started with the implementation!

# **Setting things up**

First set up the docker environment and containers:

1. Create a separate network for the containers to interact with:

```
docker network create rss
```

2. Create the postgres container with environment variables for DB name, password; expose ports, set bind mounts and working directory:

```
docker run -d --name rss-postgres \
 --net=rss \
 -e POSTGRES_DB=audioboom \
 -e POSTGRES_PASSWORD=parserssfeed \
 -p 5432:5432 \
 -v $(PWD):/home \
 -w /home  \
 postgres
```

3. Create the python container, bind mounts, set working directory and run it:

```
docker run -dt --name rss-python \
 --net=rss \
 -v $(PWD)/src:/home/src \
 -w /home/src  \
 conda/miniconda3-centos6 bash
```

4. Install the necessary libraries for python:

```
docker exec rss-python conda update -c base -c defaults conda
docker exec rss-python conda install beautifulsoup4 lxml psycopg2
docker exec rss-python conda install -c conda-forge apscheduler
```

Let’s start building our data model now…

After reviewing some of the posts, I realised there needs to be three entities:

> 1. posts: Keeping entry of each post published on the feed2. itunes_data: A post could optionally contain link to it’s itunes listing3. media: A post could 0 or more media objects present

Keeping track of these three entities pretty much contained the entire post.
Please use this ***[github link](https://github.com/vintageplayer/RSS-Parser/blob/master/create_db.sql)*** for the exact create table queries (as they are pretty straightforward)
The tables can be created in one shot by running:

```
docker exec -it rss-postgres psql -U postgres -d audioboom -f create_db.sql
```

**Helper modules**Three scripts apart from the main script were created to abstract some of the underlying functionality with function calls:

> 1. content_fetcher.py: Use to semi-robustly handle a web-page request and return it’s content2. data_parser.py: Converts the web content to a BeautifulSoup object for parsing and parses a given RSS post record in the feed and returns a dictionary of the same.3. db_connect.py: Contains DB helper functions to fetch a connection, get the count of records already present (for incremental load) and execute a given query.

Finally let’s build the script connecting all the pieces together…**1.** **Imports:** The following lines will import the required modules and objects

```
from data_parser import get_soup, parse_record, store_tags
from db_connect import get_connection, get_max_records,execute_query
from apscheduler.schedulers.blocking import BlockingScheduler
```

**2.** We’ll define some global variables also (I know not a recommended practice, but given the time constraint, it was a trade off we all have to take)

```
# Query to find the max record processed so far
get_max_query = 'SELECT COALESCE(max(itunes_episode),0) FROM tasteofindia.posts;'# Query template to insert values in any table
query_string = 'INSERT INTO tasteofindia.{0} ({1}) VALUES ({2}{3});'# List of columns present in the table
col_list  = {
 'posts'  : [<check the github script for the actual names>]
 ,'itunes_data' : [<check the github script for the actual names>]
 ,'media'  : ['itunes_episode','url','type','duration','lang','medium']
}# Creating insert queries for all the tables from template
query_strings = {k: query_string.format(k , ','.join(col_list[k]),('%s,'*(len(col_list[k])-1) ),'%s' ) for k in col_list}
```

> The column lists for posts & itunes_data is not shown. Please refer the github link for the same. It’s shown for itunes_episode to get the gist of it.

**3. begin(***feed_url***,** *db_credential_file***)**: Gets the connection of on the credential file and begins parsing the feed from feed url:

```
def begin(feed_url,db_credential_file):
 try:
  connection = get_connection(db_credential_file)
  update_feed_data(feed_url,connection)
 except Exception as e:
  print('Error Received...')
  print(e)
 finally:
  print('Closing connection')
  connection.close()
```

A simple function which starts all the ruckus and gets things moving.**4. update_feed_data(***feed***,***conn***):** requests the BeautifulSoup object for the given url and attempts to process any record in it:

```
def update_feed_data(feed,conn):
 content   = get_soup(feed)
 print(f"Processing Records for : {feed}")
 records   = content.find_all('item')
 process_records(records,conn)
 return
```

Again, following the functional paradigm, it does its job by retrieving the BeautifulSoup object and passes the content for further processing.

**5. process_records(***content***,** *conn***):** It processes records incrementally and pushes them for persistence (capturing in DB):

```
def process_records(content,conn):
  record_count = len(content)
  current_max  = get_max_records(conn,get_max_query)
  print('Current Max : ',current_max)
  records = {}  if record_count == current_max:
    print("No new records found!!")
    return records  # List comprehension on the result of map operation on records
  [persist_taste_of_india_record(conn,record) for record in map(parse_record, content[record_count-current_max-1::-1])]
```

This is the biggest function. It checks if new records are found. If yes, it first invokes ***parse_record()*** for each record, then goes ahead to persist the record.

**6. persist_tastse_of_india_record(***conn***,***data***):** It tries to persist each component of a post separately (based on the entities defined)

```
def persist_taste_of_india_record(conn,data):
  persist_record(conn,data,'posts')
  persist_record(conn,data['itunes'],'itunes_data')
  for media in data['media']:
    persist_record(conn,media,'media')
  conn.commit()
 return True
```

**conn.commit()** is necessary, else the changes in the database aren’t permanent and will be lost once the session expires.

**7. persist_record(***conn***,***data***,***tb_name***):** Execute the insert query based on the object type:

```
def persist_record(conn,data,tb_name):
 query_param  = tuple(
                list(map(lambda k : data[k],col_list[tb_name]))) execute_query(conn,query_strings[tb_name],query_param)
 return
```

***query_param*** simply stores the values in the column order in a tuple.***execute_query()*** finally inserts the data into the database

8. **Executing and scheduling it:** The script is completed by invoking the begin function and scheduling it for once everyday execution as follows:

```
if __name__ == '__main__':
  feed_url  = 'https://audioboom.com/channels/4930693.rss'
  db_credentials = 'connection.json'  print('Main Script Running...')
  begin(feed_url,db_credentials)
  scheduler = BlockingScheduler()
  scheduler.add_job(begin, 'interval',[feed_url,db_credentials], hours=24)  try:
    scheduler.start()
  except Exception as e:
    print('Stopping Schedule!!')
```

I’m using blocking scheduler here, thus the python thread is always alive. If you ever want to stop the execution, the **try…catch** block is to exit cleanly. Now you simply need to execute the main script using the following command to run it once immediately, as well as schedule it for once every day at the same time:

```
docker exec -d rss-python python main.py
```

That’s it. You have an RSS-parser ready, running every day and updating the DB.

Obviously, a lot of upgrade and enhancements are possible. Many best practices aren’t followed. SOLID principles, background scheduler, using docker compose files, etc are something to probably start with first. While building this out, I had focused on getting a functional system out first and minimal effort spent in re-factoring and designing.
Nonetheless, please do leave your comments and feel free to reach out to me here/through github.