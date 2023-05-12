# Building Analytics at 500px - Samson Hu - Medium

Created: Mar 23, 2020 5:40 PM
URL: https://medium.com/@samson_hu/building-analytics-at-500px-92e9a7005c83

![1*LnDmJMoY0xaWOZ_CG2mwDg.jpeg](Building%20Analytics%20at%20500px%20-%20Samson%20Hu%20-%20Medium%2013c54fb3ef0340fe8dfd9e5ab942496c/1LnDmJMoY0xaWOZ_CG2mwDg.jpeg)

Joining [500px](http://www.500px.com/) as Analytics Lead was a quick decision. I saw an amazing opportunity that most analysts would drool over — the chance to build an analytics function from the ground up at start-up with big ambitions. I could put into practice my vision for what a data driven company can look like.

A place where:

- Everyone understands company metrics and knows how their work fits into the measurement framework
- We measure the impact of decisions and acknowledge their success or failure
- Teams use self service tools to answer their own questions with data
- We can predict the future by digging into the data and finding leading indicators

I knew that it wouldn’t be easy. I would have to bring change to a company that was still relatively data immature. I also wouldn’t have much help.

On top of this, I would have to “change the wheels on a moving car” as all the existing infrastructure and processes still needed to be maintained.

But I’m always excited by a challenge — I signed right away.

Its now been almost a year since I joined.

Major progress has been made in rebuilding our infrastructure as well as our reporting processes. We now have a central source of truth in our [Redshift data warehouse](http://aws.amazon.com/redshift). We’ve rolled out our own business intelligence tool, [Periscope](http://www.periscope.io/), where decision makers and analysts can self serve their own analysis. And there are now reports and dashboards that are pushed to every team in the company for performance assessment.

We’re not done yet. But when you walk around the office today and see all the charts and data that appear on on people’s screens and in Slack, its clear that we’ve come a long way.

I’m going to write about the two worlds of data — the technical side and the business side. There are lots of content today about building data infrastructure. There’s also tons of articles about start-up analytics, geared towards describing what metrics metrics are important. But few people are writing about implementation and management — treating analytics as a business function.

I’m going to give my perspective.

## The Business

[500px](http://www.500px.com/) is a photo sharing community and stock photography marketplace. Our platform includes a desktop and mobile website, mobile applications on Android and iOS, as well as third party applications such as Flipboard. We’re backed by world class investors that include [Andreessen Horowitz](http://a16z.com/) and [ff Venture Capital](http://ffvc.com/).

Our two revenue streams are:

- Paid subscriptions that allow users to upload more photos
- A stock photography marketplace where we take a cut of each sale

Several teams run the company. Our development teams include web, mobile, and platform. On the non technical side, we have sales, marketing, content, customer excellence, and product. At the top, we have an executive leadership team. In total, our headcount sits at over 60.

Every team has their own work styles and requires analytics in order to function at their best. For example, executives meet once a week on Tuesdays to discuss high level strategy. Having a clear summary of where the metrics are headed at this meeting is crucial for top level decision making.

Even for technical people, having access to analytics is helpful. Being informed about product metrics helps developers see the ‘why’ behind their work — a key ingredient to high performance.

## The Tech Stack

All our apps and websites run on top of our API servers. On these servers, we serve a monolithic Rails application as well as a handful of microservices. These are backed by several databases, the main one being MySQL.

On MySQL, we store stateful information that is used by our applications. Two tables of importance are the photos and users tables. We also have a table for subscription purchases and stock photography purchases.

We log API calls and state changes in the backend. For example, a call to serve a photo is logged, as well as an action such as a signup, upload, vote, or follow.

In case you don’t know, logs are just text files. When we log an action, we simply append a line that looks like this:

> 2015–02–10 10:24:31.32444 23432423 photo_like 423223 123.132.623.123 /get?…

Items in a line can include the timestamp, photo id, user id, user ip, action as well as anything else that is relevant.

These provide a history of activity on our platform that complements the stateful information that we have in MySQL. These logs are aggregated and archived in S3, hourly. We produce around 20gb of log files a day.

Both these data sources, MySQL and the logs, are useful for analytics. MySQL is great for grabbing photo and user information, as well as stock photo and subscription transactions. The logs are great for understanding user behaviour over time.

Now that you know a little bit about the company and our technology, lets take a look at the evolution of our analytics.

## Two Sources of Data

When I first started, I was presented with two sources of data that I could work with: Splunk and MySQL.

MySQL could give states like the total number of likes on a single photo, but it couldn’t tell me how many likes the photo got in the last hour.

Splunk is a log search engine on top of logs. Wait… what does that mean?

Logs can tell you a lot about user behaviour. When a user likes a photo, that action is written to a log file and provides a timestamped record. So by looking at the logs, you can get an answer to how many likes a photo got in the last hour by going through and counting every line where you see a like event on that particular photo.

But log files are just text files. Getting value out of them is difficult since they need to be parsed. This is where Splunk comes in.

Splunk is a tool that allows you to search and analyze log data. I could ask questions about user behaviour:

- On average, how many photos does a user upload in a single session?
- How many android users used our platform in the last month?

Splunk would then go through the logs line by line very quickly, and count the number of events that match the query.

## Two Headaches

Querying these two sources was simple enough. If I wanted stateful information, I would query MySQL. If I wanted to know about user behaviour over time, query Splunk.

But when you needed to ask a question that involves both behaviour and state, such as how many users liked a photo in the last month (Splunk), broken down by user subscription type (MySQL), you would need an offline way to query the two data sources separately and then combine the two. For this, I used Python with its MySQL and Splunk libraries.

This was a minor headache.

It was not time efficient to write custom code to do data pulls.

There was also a much bigger headache

These two data sources were not user friendly. Splunk has a special query language that has few resources online. The schemas in MySQL were not well documented. This put the responsibility of pulling data solely on the analyst.

When there’s only one analyst for a company of over 60 people who all need to access data and can’t do it themselves, its going to be a bad time.

## The Exec Dashboard — Run For The Hills

The situation was not much better in metrics reporting.

We used Splunk to count the number of events (signups, uploads, etc) by date and client (web, iphone, android, etc). The result of these Splunk searches were stored in a Google Sheet dubbed the Exec Dashboard, called by a script which ran nightly:

Our Exec Dashboard. Numbers have been randomized

Imagine combing through a thousand numbers in order to understand how basic metrics like daily active users were trending. Only the most seasoned MBA’s on our team could keep up.

It was clear that some things needed to change.

For one, the data was not accessible. I was becoming swamped with data pulls Four months in and I might have well renamed my job title to Data Monkey. It was hard to blame the infrastructure, especially as I was new.

And secondly, it was hard to know how the product and company were doing. Very few people could understand our metrics. The Exec Dashboard was a disaster.

I had to act. I needed to rebuild the infrastructure while maintaining current reporting processes. As well, I had to manage the flow of requests for data from around the company and make sure data is still flowing, but that I would have enough time to spend on infrastructure work.

After the infrastructure was built, I needed to redo the reporting, and evangelize the new system to the rest of the company.

At this point in the company, a new infrastructure project that didn’t lead to moving the needle on metrics was the last thing the executive team wanted to hear. But it was necessary. I gambled that I could do all this and demonstrate value before they lost their patience.

This is why I love start-ups. You can do stuff like this. #yolo

On the infrastructure side, I needed two things:

- A database that combines the logs and MySQL that is easy to query
- A front end to this database. Something that is easy to use so that anyone can query the data model with minimal help

With this, I could remove myself from being a dependency to all data analysis and pulls around the company.

Fortunately, we don’t have to reinvent the wheel. There exists products which solve exactly these two needs. In the next two sections I’m going to talk about implementing the Redshift database and Periscope.

Afterwards, I’ll talk about rebuilding metrics reporting using Periscope and Google Sheets.

# New Infrastructure, Part 1 — Redshift

I’m going to go deep in this section into data warehousing. If you already are familiar with this concept, feel free to skim to the next section.

## A Primer on Dimensionality Modelling

Kimball introduced in the 90's the idea of the dimensional data warehouse. This is a SQL database specialized for business analysis, different than production databases for applications. It is meant to be easy to understand and query.

Dimensional data warehouses have a special schema, with two types of tables called *fact tables* and *dimension tables.* Data would flow from the source (MySQL and logs), to these two types of tables in a process called Extract-Transform-Load (ETL).

Lets briefly talk about ETL and the schema.

## The Dimensional Data Warehouse Schema

The schemas of data warehouses have two types of tables:

- *Fact tables* record measurements in time of a process.
- *Dimension tables* record information about a particular item.

Both tables are meant to be understandable. They must have readable column names and values.

As an example:

- The *likes fact table* has the columns: datetime, user_id, photo_id, client
- The *users dimension table* has the columns: user_id, username, first_name, last_name, …, subscription_type, …, is_seller, …, has_android_app, …

Here’s an example of using this schema.

If we wanted to know how many likes in the past week, we could query the *likes fact table*, sum the records, and filter by date.

But if we wanted a breakdown of likes by user subscription type, querying the *fact table* would not be enough. subscription_type is not contained in the *likes fact table*. But user_id is. We would need to join the *likes fact table* to the *users dimension table* by user_id, and then group by user subscription_type.

From this example, its easy to understand why *fact tables* often contain foreign keys to *dimension tables*. This is so that they can be joined so that facts can be sliced by dimensions.

## ETL

In order to populate our data warehouse with data from our production databases and logs, we apply a process called ETL.

Data warehouses look very different than production databases and log files. Tables are often denormalized, and complexity is hidden. For example, in production to see if a user has an active subscription, we might need to write a complex query involving several tables. But in a data warehouse, it should simply be a yes/no column in the users table.

Because of this, we need to transform the data after we extract it from its source and loading it to the data warehouse. Hence the name E-T-L.

By hiding a lot of the complexity to querying the data in the ETL, accessing data becomes much easier and fewer mistakes are made.

## Creating The Schema

By this time I had spent a few months pulling data and doing ad hoc analysis. Looking at my past queries, I came up with a set of table requirements:

- **Fact Tables**: Subscription purchases, stock purchases, uploads, signups, likes, favourites, follows, …
- **Dimension Tables**: Users, Photos

This seemed to walk the line between not fulfilling enough requirements and over-engineering the system.

## Does This Schema Fit Our Needs?

This data model contains both log and MySQL data — in a single place where no extra work needs to be done to combine them. It is simple to understand and read. All the complex queries such as determining the account type of a user that I used to do are now hidden in the ETL. Querying this data model is a pleasure.

But sometimes our data model falls short:

1. If we don’t have the right table set up for our question
2. If we need fancy processing that goes beyond SQL

With proper planning and iterating on our solution, we minimize 1).

SQL is powerful. Questions in the form of 2) are complex, and are often beyond the scope of a business intelligence platform.

## Hosting It — Amazon Redshift

Now that we talked a bit about the schema for our data warehouse, we need an actual database to host it.

There are technical requirements for databases that can support a dimensional model.

The main operations on such a database are aggregations and joins. These two operations are expensive on traditional databases, intended to be the data store for applications. Try joining a 100m table to a 500m table in MySQL. Even Postgres would buckle. We needed something specialized.

We needed something specialized for analytics use. Luckily for us there exists a cheap, easy to use, easy to maintain database that is optimized for analytical queries such as joins and aggregations: Amazon Redshift on AWS.

A Redshift database with 2tb of disk space, sufficient for our needs, costs a little over $4000 a year.

## Building the ETL

**Repeat after me: I will not bake my own ETL solution.**

ETL pipelines get very messy very quickly. You will find that your production database isn’t all that well thought out. Getting certain kinds of information needed for the ETL will require hacks and lots of dependencies.

> For example, a major headache for our metrics is measuring subscriptions, renewals, and churn. If a user with an existing subscription purchases a new one manually (not auto-renewed) to extend his subscription, then originally in our code we counted this as a new subscription. But since he was already a subscriber, we would be double counting him. So therefore we need a way to see if someone that buys new subscription was already a subscriber, and if he is throw him in the renewals bucket.But there is no such column in MySQL. Since we are doing this calculation once a night, by the time a person extends their subscription we no longer have the ability to check if we was previously an active subscriber. The only column we have is is_active. So we need to create a new table used only by our ETL which stores a record of active subscribers on a certain day. We left join against this table and remove those that were previously active, to get our fixed new subscribers count. We do a similar thing to add him to renewals.

Did you follow that?

Production schemas are awful for analytics.

An ETL script that has to turn messy production data into clean data warehouse data will naturally be extremely messy.

Use a framework like [Luigi](http://luigi.readthedocs.org/en/stable/) or a tool like [Informatica](https://www.informatica.com/). These have well known coding styles and constructs, and are also widely used. It will still be messy. But it will be comparable to known ways of doing ETL.

If you ignore this advice and end up baking your own, nobody will be able to understand the system once you leave.

I chose the Luigi framework to build the ETL pipelines on for many reasons:

- Luigi is built and supported by Spotify. It is used by thousands of start-ups around the world. There is an active mailing list and a growing community.
- Luigi is open source and extendable. Its clear what is going on, and extending the base classes are encouraged.
- Luigi is Python based, a popular language for handling data.
- The code for Luigi is very readable. The basic unit of Luigi are task classes that model an atomic ETL operation. They have three parts. A requirements part that includes pointers to other tasks that need to run before this task, the data transformation step, and the output. Each task is thus a node in a directed graph — the ETL job. Luigi will actually visualize this graph for you in its visualizer, and give you diagnostic information about each run of the ETL.
- Structuring the code this way makes things easier to read and maintain. There’s both hierarchy and relationships. I also put all the tasks that feed into a final table on Redshift into one file. This allows me to quickly see the structure of the code, and isolate the pieces that I’m interested in.

The Luigi directed graph

- Luigi is idempotent. Meaning running it twice one after the other won’t do anything. It will only re-run parts of the code again if you remove the output of those particular tasks. This is supremely helpful in debugging. If a run fails at a particular node, you simply have to fix that node, before hitting run again. You don’t have to isolate that piece of code, and painstakingly run it in isolation.
- Luigi has error logging and status emails. You get a notification if a node fails during a run. You can then view the error stack trace, fix the code and rerun the ETL.

After writing the ETL in Luigi, I had over 200 nodes in the directed graph. These actions include pulling data from MySQL, uploading the dump to S3, and then loading them to Redshift from S3. One specific node triggers an Elastic Mapreduce instance to parse the log data and transform them into fact table dumps stored on S3, which are then loaded onto Redshift.

A whole run of the ETL takes around four hours from start to finish. I set the process to start at midnight every night.

## The Finished Data Warehouse

So that’s our data model — stored on Amazon Redshift, and fed new data every night by ETL pipelines run on Luigi.

At first after implementation, you’ll realize you’ll have missed a few things in the requirements. People will ask you for of changes to the schema as they need that one extra column for their analysis. You will notice parts of the ETL breaking as engineering makes changes to the production schema without telling you.

But after a while things will stabilize. People will stop requesting changes. You will get used to the cadence in which engineering changes the production schema. Engineering will also get better at communicating to you when schema changes do happen.

There’s a few things you can do to make sure that the data in the data warehouse is accurate. I’ll talk about these later in this article.

All in all, running this data warehouse costs less than $8000 a year. A bargain compared to traditional data warehousing solutions for this scale.

# New Infrastructure, Part 2 — Periscope

With the data warehouse built, there was now a need for a tool that could be used around the company to access it. I evaluated several popular options.

- The simplest and cheapest solution would have been to give everyone a SQL terminal. But its not easy or friendly to use, and there was still friction to learning SQL.
- Looker was really enticing, as its interface allowed for non technical users to access the database and build dashboards and reports. But paying 30k+ a year was outside of our budget.
- Tableau was a powerful tool for visual analysis, but its falls short outside this range. It can’t do reporting and list pulls very easily. It also needs to store data in memory before computing, rather than relying on Redshift’s excellent data processing abilities.

None of these solutions fit. I found my answer in [Periscope](http://www.periscope.io/), an early stage start-up that built a product which was exactly what I was looking for.

- Periscope is a lightweight analytics tool where you can write SQL to create charts.
- Periscope can connect to Redshift easily as they are both cloud solutions.
- The dashboard is the basic document type.

An example of a dashboard

- On these dashboards users can write SQL to create charts and tables.

Writing SQL to create charts

- It is collaborative. Unlimited users can sign up within a company and see each other’s dashboards. Links can be sent to other users in Slack and email to point them towards certain dashboards.
- Each dashboard updates hourly automatically so you get current data.
- You can set each dashboard to send itself out as an email at set times.

This tool is killer:

- It is SQL based so learning SQL is a requirement. But by making dashboards so easy to share, using Periscope became a social activity inside the company. This created a strong incentive for people to learn SQL.
- Ad hoc analysis in Periscope is fast. Because its so quick to create charts, you can iterate quickly on how you are trying to look at the data and what questions you are asking. I feel that iteration is the most natural mode of work for an analyst. By making iterations fast, you get to the answer you are looking for much faster.
- Reporting in Periscope is easy. To pull a list, simply create a new dashboard, write your SQL, and hit save. You can then share a link to the dashboard or export the table as a CSV.
- Periscope is a full featured dashboard tool. One of the first things I did after I set up Periscope is to build dashboards for each product and team that we have. I then set these dashboards to email everyone each morning.
- Periscope is collaborative. Everyone in the company can join and see what everyone else is working on. Users can add charts to each others dashboards, or edit the SQL behind each other’s existing charts. Users that are stuck with a query can quickly and easily ask for help.
- The cost was reasonable. For a company of over 60 people, I was happy at the monthly price that we were charged.

After setting up Periscope, a new channel of communication opened up inside the company — a data communication layer.

I was no longer a dependency in allowing data to flow around the company. This freed up much of the time I was spending doing data pulls. And the company as a whole is now looking at more data we were when I was soloing data pulls and analysis.

Implementing Redshift and Periscope was a major success.

## Deciding on Format

With the infrastructure done, we now needed to focus on fixing metrics reporting. The old Google Sheets Exec Dashboard, with its thousands of numbers, needed an overhaul.

Not only was it hard to understand, but it was also one size fit all. Executives didn’t need daily numbers unless there was a big outlier. Marketing didn’t need as much detail on product metrics and product didn’t need as much detail on marketing metrics. Nobody on the development team could understand what was going on.

There was also the issue of metrics definitions. Not everyone understood what we considered to be a daily active user. This was a problem.

A new set of dashboards needed to be created. Ones that are easier to understand and make decisions from, and customized to each team. Ones that are documented so that everyone is on the same page with what we are measuring.

I started at the top, first working on the dashboard which would serve the executive team. This would be in the form of a weekly tearsheet of metrics to be handed out at the executive meeting every Tuesday. I worked closely with our VP Product and VP Operations, iterating on different ways that the company can be measured.

We went back and forth and iterated over a few solutions. Over a few weeks, the format was settled. The tearsheet would list out the most important metrics relevant to each team. The tearsheet would go back five weeks.

In separate tabs, each metric in this document would be clearly documented with precise definitions.

Next to each weekly number, there would also be a projected number, drawn from our master planning document. We could compare the two to see if we are on track with our overall strategy.

This exec tearsheet is our most important dashboard. It lays the foundation for how people at 500px should be thinking about their work. From this tearsheet, dashboards for the other teams followed.

I ended up creating a set of dashboards for each of the following teams:

- Product
- Web
- Mobile
- Marketing
- Sales

These dashboards were done in Periscope and were visual. Each dashboard included the metrics that the teams were responsible for in the exec tearsheet, and also included other supporting metrics. There would be one chart per metric, usually a line chart. Each chart had definitions included with it, so users can hover over over the info icon next to the chart and read the definition.

There were two ways to access these dashboards. Users can log in to see their dashboards anytime they need to. But I also set Periscope to email each team their dashboards every morning.

Emailing dashboards out was especially helpful to developers. They didn’t need to log into Periscope very often and thus didn’t need to build the habit. They can get everything they need through email.

## On Defining Metrics

There are better resources than my own experience for how to measure companies. But I will talk briefly about the themes for each dashboard.

At the executive level, the tearsheet includes metrics that are mostly daily averages by week. This makes it easy to stay within one frame of reference, for example when comparing against daily counts of active users.

The metrics that we measure exist in relation to our engagement funnels. You can think of three funnels at 500px:

- visitor -> signup -> daily active -> daily engaged -> paid subscriber
- visitor -> signup -> photo upload -> photo submit to marketplace -> photo sold on marketplace
- visitor -> signup -> purchase photo from marketplace

Each team owns different parts of this funnel for different products:

- The marketing teams own (page views) and the top and bottom (revenue) of this funnel
- The product teams has less of an emphasis on top of funnel metrics
- The development teams (web and mobile), want to see the entire funnel with respect to their own products.

The book Lean Analytics promotes the use of ratios (uploads/dau per date) over counts (uploads per date). Our team decided that counts would be easier to socialize up and down the leadership chain.

Counts are used for everything except product metrics, where we focus on measuring features in two ways:

1. Frequency of use (# of times a user uploads photos a month)
2. Magnitude of use (# of photos per upload)

Rolling out the infrastructure and new measurement system requires training. People need to learn how to use Periscope and have a clear idea of what the metrics are all about.

## Periscope Training

Periscope is based on SQL, so people need to know how to write SQL to use it effectively. There’s two great resources that I point people to:

Once SQL skills are acquired, then I give them the Schema Definitions Document. In this Google Sheet I define every table and column in the data warehouse. If a column is categorical, I list its possible values.

## Metrics Evangelism

Just giving everyone dashboards and reports is not enough. Everyone needs to get on the same page with respect to what we are measuring.

I hosted an hour long lunch and learn where I described the measurement framework to the entire company. I spent a good 45 minutes talking about every metric that we use. I tried my best to be fun and engaging in the light of such dry material.

This is necessary. Not everyone knows what a daily active user is. Its not obvious. There is great confusion when dozens of metrics are thrown around but there’s no consensus on definitions.

On top of this, for a company to be data driven, everyone needs to know how their work fits with respect to the metrics. So metrics needs to be ingrained in the culture, talked about from when people set their quarterly objectives to when problems are solved tactically.

The communications campaign needs to be ongoing.

Metrics are often wrong. I think this is something that is often not talked about as much publicly out of general embarrassment. But every company faces this.

There’s so much room for failure in this system:

- Logs could get parsed wrong, and you undercount or over-count an event
- The log sender on an API server could fail and you don’t notice and you miss a fraction of your events
- There might be network issues one day, and 10% of your log entries might fail to send to S3
- Some metrics that are important might be hard to query in the database and you might pull the wrong number
- etc

This doesn’t include hard fail events like your ETL’s failing and the metrics not being refreshed. These errors are silent.

Errors will happen. Someones butt is gonna get kicked every time metrics need to be restated to the board. But its hard to avoid completely.

How do you combat this?

Always be auditing.

Tie important numbers to external sources of truth. We pull Daily Active Users from our data warehouse and compare them against Google Analytics daily. We also do a match of our subscription metrics to Stripe/Paypal.

We also cross reference the fact tables that we create from the logs, to the dimension tables that we create from MySQL. This is a check against parse errors. For example, we compare new users in our users dimension table, to signup events in the signups fact table.

Lastly, we rely on our teams to report when they think the metrics look funny. Unexplainable outliers, jumps or dips in numbers, or a pair of inconsistent metrics — these are all signals that something might be wrong.

But the system is still crazy complex and hard to QA. After talking to people in analytics roles at many different companies, realistically you should trust your numbers at most with an 80% degree of confidence.

This is a hard truth to swallow.

Analytics is a partnership between several business units: product, marketing, customer support, sales, and engineering.

In particular, care must be taken to manage the relationship with engineering.

Analytics needs to be on the engineering roadmap. At each feature release:

- data models need to be easily queried for analytics
- event logging needs to be put in for relevant user actions

At the same time, analysts need to be aware of how engineers work. They need to know the cadence of the sprints, how work is distributed on the teams, and how best to put in requests for engineering time.

I was fortunate that as my needs grew, engineering and product were both considerate. On my side, I had a bit to learn about how to work with established engineering teams.

Its funny. Considering that in my last role I sold software to tech companies, I greatly underestimated how much selling this role would need.

Without the right structure, the work that analysts do is hard to understand. They are alone in an organization, drifting from team to team, project to project. Its hard to stay motivated without visibility and a support network.

I’ll give you my own experience.

My plan at 500px was to build analytics in stages:

1. infrastructure
2. reporting
3. analytics
4. predictive modelling

Analytics, the part where analysts dig deep into the data to figure out the business, wouldn’t be effective to do until reporting and the infrastructure were fixed.

But when questions from the top start floating to you about why you aren’t doing your job — why the analytics part isn’t being done, and you are still working on building out the infrastructure, its highly demotivating. Its hard to push back unless you had buy-in into your roadmap in the first place.

Time also needs to be spent communicating wins. People need to feel excited about the progress happening on the data front. It helps with getting stuff done that you need help on, and keeping politics off your back.

People don’t naturally get data, why its important, and how its done. All three are important to the success of the analyst.

If I had to do anything differently, or next time, I would allocate 20% of my time towards evangelism. Building processes for communication. Lunch and learns. Presentations. Socialising. Selling.

Spend 20% of your time selling. Its important.

In the past year, we’ve fixed the data infrastructure and have a sane reporting system. We’ve rolled this out to the company, with training and socialization.

Hurdles faced along the way included dealing with lack of resources, and inter company politics. But they didn’t stop us from getting things done.

We now have a system where people know how the company is doing, and can self serve their own analysis and data pulls without asking the analyst. We’re far from where we started and well on our way to transforming 500px into a top data-driven start-up.

## What’s Next?

What a year. We haven’t even scratched the surface yet with respect to analytics. There’s so much more to do:

1. Front end analytics like Google Analytics aren’t well understood
2. Modelling out the whole pirate metrics by channel
3. Segmentation of our user base
4. Causal modelling for the impact of feature changes
5. Creating a LTV model to use for marketing
6. A process for A/B testing
7. Expanding the team

Its going to be an exciting time.

But I’m stepping away from my role. My plan for coming into 500px was always that it would be temporary, and that I would eventually move west to San Francisco.

In July, I will be moving to SF to join [Wish](http://www.wish.com/). I’ll be working on their data platform.

I’m excited to head to tech mecca. And I’m looking to meet others that are interested in data.

If you want to grab coffee in SF, or are interested in replacing me at 500px (we are looking for a senior data engineer, business analyst, and data analyst), send me a message at shanzhen.hu@gmail.com. All jobs are posted at [https://500px.com/jobs](https://500px.com/jobs).

*Thanks to [@josephby](https://twitter.com/josephby) for being a great boss, [@andyyangstar](https://twitter.com/andyyangstar) for bringing me in, Kevin Martin for taking over the infrastructure after I left, @robbraun for showing me how Uken Games implented its analytics infrastructure*, *and [@seanpower](https://twitter.com/seanpower) for a great talk about data. Its been a good year.*