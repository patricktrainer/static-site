# Adding Faust to your Existing Architecture - Robinhood Engineering

Created: Jun 12, 2020 10:58 PM
URL: https://robinhood.engineering/adding-faust-to-your-existing-architecture-39b0ebd1f7c9

A few weeks ago we [open sourced](https://robinhood.engineering/faust-stream-processing-for-python-a66d3a51212d) [Faust](https://github.com/robinhood/faust), a Python stream processing library that we built at [Robinhood](https://robinhood.com/) to make it extremely easy to build and deploy traditionally complex streaming architectures.

As Robinhood has grown and we have added more and more functionality to our product, our infrastructure has also evolved. We have added numerous internal services and technologies to help us solve different problems. This has resulted in a typical application often needing to interact with one or many different services.

Typical streaming frameworks such as [Spark](https://spark.apache.org/streaming/) require external dependencies to be packaged with the app in specific ways, and submitted into the [Yarn](https://hadoop.apache.org/docs/current/hadoop-yarn/hadoop-yarn-site/YARN.html)/[Mesos](http://mesos.apache.org/) cluster that is running the application. This is usually a detour from how Python applications typically manage dependencies — [virtualenv and pip](https://docs.python-guide.org/dev/virtualenvs/).

We built Faust as a library to allow for it to be used with any existing tools you may be using. Simply install Faust, and use it to develop Python applications as you typically would. We use [Python Asyncio](https://medium.freecodecamp.org/a-guide-to-asynchronous-programming-in-python-with-asyncio-232e2afa44f6) to achieve high performance I/O.

In this blog post we will walk through some examples of how we use Faust to interact with various different services using off-the-shelf libraries.

[Redis](https://redis.io/) has established itself as an in-memory data store of choice owing to its [data structures](https://redis.io/topics/data-types), amazing query speeds and simplicity. We use Redis on Robinhood’s Data team across a variety of use cases. Following is an example, showing how we use Redis to cache messages on the Robinhood Feed.

We can install [aredis](https://github.com/NoneGG/aredis) and Faust using pip:

```
pip install aredis
pip install faust
```

Upon installing the dependencies, let’s first define our Faust application, Kafka topic and models:

```
import datetime
import faustclass Activity(faust.Record, isodates=True):
    user: str
    message: str
    timestamp: datetime.datetimeapp = faust.App("redis_example", broker="kafka://localhost:9092")
activities_topic = app.topic("feed_activities", value_type=Activity)
```

We can now create an [agent](http://faust.readthedocs.io/en/latest/userguide/agents.html) which reads feed activities coming in through this topic, and adds the messages to the user’s Redis sorted set as follows:

```
@app.agent(activities_topic)
async def save_activities(activities):
    async for activity in activities:
        client = aredis.StrictRedis(host="localhost", port=6379)
        await client.zadd(activity.user, activity.timestamp, activity.message)
```

As shown above, we use Redis as you would use it in any app. Faust doesn’t require any special drivers or modes for using Redis. All it needs is a Redis library that’s compatible with Python Asyncio.

We often use streaming apps that need to talk to other services over HTTP. Below is an example of how we use the Python [aiohttp](https://aiohttp.readthedocs.io/en/stable/index.html) library from a Faust streaming app for one of our use cases at Robinhood.

First, let us install the Python library we will use for HTTP requests:

```
pip install aiohttp
```

We skip the app and model definition which is similar to the previous, and straightaway look at how we would design our agent. We create an agent which processes orders and uses a third part HTTP API to send order confirmation emails to our customers:

```
async def send_confirmation(order):
    url = f"https://emailer.robinhood.com/"
    data = {
        "user": order.user_id,
        "subject": "Order Confirmation",
        "body" f"Order: {order.quantity} shares of {order.symbol}",
    }
    async with aiohttp.ClientSession() as session:
        await session.post(url, json=data)@app.agent(orders_topic)
async def add_symbol(orders):
    async for order in orders:
        await send_confirmation(order)
```

A lot of our internal services export REST APIs. The ability to easily integrate aiohttp with Faust apps allows us to break down a variety of our backend systems into simple and isolated streaming apps.

Robinhood operates on large amounts of time series data such as tick by tick price data for each stock symbol. We use [InfluxDB](https://www.influxdata.com/) to store some of these time series. Below is an example of how we query InfluxDB from a Faust application.

Again, as before, let us install the Python library we will use to query InfluxDB:

```
pip install aioinflux
```

We now create an agent which looks at the orders topic from above and looks at the time series in InfluxDB for the particular stock to get the price at which the order executed was the price in the market at the time. We do this to ensure that we are giving the best quality of executions to our customers.

```
@app.agent(orders_topic)
async def add_symbol(orders):
    async for order in orders:
        client = aioinflux.InfluxDBClient()
        query = f"SELECT price FROM marketdata WHERE symbol = {order.symbol} AND timestamp <= {order.timestamp} ORDER BY DESC LIMIT 1"
        order.market_price = await client.query(query)
        await quality_topic.send(key=order.id, value=order)
```

The ability to easily integrate streaming apps with InfluxDB lets us solve problems where we need to work with multiple time series.

The data team at Robinhood uses the [ELK (Elasticsearch-Logstash-Kibana)](https://www.elastic.co/elk-stack) stack quite extensively. Last year, we published a [post](https://robinhood.engineering/taming-elk-4e1349f077c3) about how we use the ELK stack along with Kafka. Below is an example of how you can query Elasticsearch from your Faust app.

We first install the [elasticsearcy-py-async](https://github.com/elastic/elasticsearch-py-async) library that we will use in this example:

```
pip install elasticsearch-async
```

We now create an agent which looks at incoming search queries and adds the top search result from our search service running on top of Elasticsearch.

```
async def get_top_result(query_string):
    client = elasticsearch_async.AsyncElasticsearch()
    query = {"query": query_string}
    resp = await client.search(index="search_index", body=query)
    return resp["hits"]["hits"]@app.agent(search_queries_topic)
async def add_top_search_result(search_queries):
    async for query in search_queries:
        query.top_result = await get_top_result(query.query_string)
        await top_results_topic.send(key=query.top_result, value=query)
```

Faust makes it easy for us to build architectures where we use Elasticsearch as our data store of choice.

The above examples show how we use Faust with external dependencies, across several use cases. In the coming weeks we will go deeper into some of the specific ways we use Faust.

Faust works well with most common Python libraries making it very easy to use with any existing applications. We’re very excited to see how developers will use Faust, and what use cases they will come up with.

Please feel free to leave a comment here or a note on [Github](https://github.com/robinhood/faust) if you have any questions or thoughts. We’re also [hiring](https://careers.robinhood.com/)!