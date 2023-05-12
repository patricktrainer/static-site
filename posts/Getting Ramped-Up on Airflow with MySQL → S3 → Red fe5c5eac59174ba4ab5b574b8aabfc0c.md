# Getting Ramped-Up on Airflow with MySQL → S3 → Redshift - By Austin Gibbons

Created: Jan 28, 2020 8:06 PM
Tags: Data
URL: https://hackernoon.com/getting-ramped-up-on-airflow-with-mysql-s3-redshift-defcc4522c8c

I recently joined [Plaid](https://www.plaid.com/) as a data engineer and was getting ramped up on [Airflow](https://medium.com/airbnb-engineering/airflow-a-workflow-management-platform-46318b977fd8), a workflow tool that we used to manage ETL pipelines internally. If you’re totally new to Airflow, imagine it as a souped-up crontab with a much better UI.

![Getting%20Ramped-Up%20on%20Airflow%20with%20MySQL%20%E2%86%92%20S3%20%E2%86%92%20Red%20fe5c5eac59174ba4ab5b574b8aabfc0c/1Zd-Z796er5lxaFW81EaWGA.png](Getting%20Ramped-Up%20on%20Airflow%20with%20MySQL%20%E2%86%92%20S3%20%E2%86%92%20Red%20fe5c5eac59174ba4ab5b574b8aabfc0c/1Zd-Z796er5lxaFW81EaWGA.png)

It’s fast! It’s flexible! It’s free! It’s Airflow!

Around the time that I was joining, Plaid was migrating onto [Periscope Data](https://www.periscopedata.com/) for visualizing SQL queries, and my immediate mission became to get more of the data people relied on for analytics insights into our nascent [Redshift](https://hackernoon.com/tagged/redshift) cluster, the data warehouse we query from Periscope. My colleague had spent some time harvesting our MongoDB tables into Redshift by tailing the oplogs and doing some post-processing in Spark, as well as parsing through a bunch of log dumps in S3 to create meaningful analytics tables.

[Getting%20Ramped-Up%20on%20Airflow%20with%20MySQL%20%E2%86%92%20S3%20%E2%86%92%20Red%20fe5c5eac59174ba4ab5b574b8aabfc0c/0Dt4pTxhZXWN8CtwF](Getting%20Ramped-Up%20on%20Airflow%20with%20MySQL%20%E2%86%92%20S3%20%E2%86%92%20Red%20fe5c5eac59174ba4ab5b574b8aabfc0c/0Dt4pTxhZXWN8CtwF)

Plaid ETL pipeline circa early 2018

### Motivation

Kindly, my coworker left a more straightforward task to me to help me get ramped up with Airflow — moving data regularly from MySQL to Redshift. We had recently begun using Amazon Aurora instances on RDS, and needed to harvest the data from RDS and load it into Redshift to establish KPIs for these new datasets.

[Getting%20Ramped-Up%20on%20Airflow%20with%20MySQL%20%E2%86%92%20S3%20%E2%86%92%20Red%20fe5c5eac59174ba4ab5b574b8aabfc0c/00hMmiPfougfcSfmz](Getting%20Ramped-Up%20on%20Airflow%20with%20MySQL%20%E2%86%92%20S3%20%E2%86%92%20Red%20fe5c5eac59174ba4ab5b574b8aabfc0c/00hMmiPfougfcSfmz)

Our goal was to timeframe this exercise to a week, so we set ourselves some constraints:

1. We were going to use MySQL’s ability to select into s3, and Redshift’s UNLOAD command.
2. We would only perform complete table-copies once every day, for every table. Since our largest table took only a few hours to copy, we decided to accept pulling all of the data every night as both easier to implement and more resilient to changes or incongruities in the two data sources.
3. We would work on getting the most important data, and not worry about details like deeply nested json columns or binary image files stored in the database.

### Designing a workflow

We wanted to design a translation from MySQL to Redshift, and knew that there would have to be a translation of the schema. Fortunately, AWS provides a resource [comparing MySQL and Redshift types.](https://docs.aws.amazon.com/datapipeline/latest/DeveloperGuide/dp-template-redshift.html) We can pull the schema out of MySQL using a straightforward query:

```
selectfromwhere
```

We handled a few types manually, for example instead of moving binary data over we would detect a binary type and instead return a boolean as for whether the column was null or non-null, to avoid having to copy a large amount of binary data over the wire that would be unusable for analytics. We wrapped the functionality into some python scripts that generates translation configurations.

[Getting%20Ramped-Up%20on%20Airflow%20with%20MySQL%20%E2%86%92%20S3%20%E2%86%92%20Red%20fe5c5eac59174ba4ab5b574b8aabfc0c/0Nx5B0xgn3StVNWDS](Getting%20Ramped-Up%20on%20Airflow%20with%20MySQL%20%E2%86%92%20S3%20%E2%86%92%20Red%20fe5c5eac59174ba4ab5b574b8aabfc0c/0Nx5B0xgn3StVNWDS)

Example MySQL configuration

We then created dag_mysql_processor.py to take in these database configurations and generate the associated dags. It iterates through each entry and generates the corresponding step using a series of SQL templates that we wrote using the [AWS Docs](https://docs.aws.amazon.com/redshift/latest/dg/r_UNLOAD.html) as a guide. For example:

[Getting%20Ramped-Up%20on%20Airflow%20with%20MySQL%20%E2%86%92%20S3%20%E2%86%92%20Red%20fe5c5eac59174ba4ab5b574b8aabfc0c/0ikFXRIHAMiyyWScJ](Getting%20Ramped-Up%20on%20Airflow%20with%20MySQL%20%E2%86%92%20S3%20%E2%86%92%20Red%20fe5c5eac59174ba4ab5b574b8aabfc0c/0ikFXRIHAMiyyWScJ)

The result is a batch of Airflow DAGs, one for each table in a MySQL Database. Currently we have each of these DAGs running once daily, which provides a good-enough latency for our current use-cases, by completely re-building the table once a day.

![Getting%20Ramped-Up%20on%20Airflow%20with%20MySQL%20%E2%86%92%20S3%20%E2%86%92%20Red%20fe5c5eac59174ba4ab5b574b8aabfc0c/1bslSQlbJWpEU6gLVQEcBhQ.png](Getting%20Ramped-Up%20on%20Airflow%20with%20MySQL%20%E2%86%92%20S3%20%E2%86%92%20Red%20fe5c5eac59174ba4ab5b574b8aabfc0c/1bslSQlbJWpEU6gLVQEcBhQ.png)

Our linear DAG pulling data from MySQL to S3 to Redshift

### Bumps in the Road

The first bit of trouble came about from trying to do a hot-swap. We wanted to ensure that the table looked correct before replacing the old data, so we added a step to validate the row counts. In the first version of our DAG, we executed each statement as a separate airflow task, but tables could occasionally disappear. Combining the swap step into a single, transactional task prevents any table downtime for our style of full-table replacement.

![Getting%20Ramped-Up%20on%20Airflow%20with%20MySQL%20%E2%86%92%20S3%20%E2%86%92%20Red%20fe5c5eac59174ba4ab5b574b8aabfc0c/1NvjBzDLxrkNvLFWPAhj8OQ.png](Getting%20Ramped-Up%20on%20Airflow%20with%20MySQL%20%E2%86%92%20S3%20%E2%86%92%20Red%20fe5c5eac59174ba4ab5b574b8aabfc0c/1NvjBzDLxrkNvLFWPAhj8OQ.png)

V1 of the project had a race condition in dropping and recreating the table.

We anticipated that full-copies would be troublesome, as some of our tables are many billions of rows and a global “success or fail” — a consequence of only doing full table copies — would be hard to recover from in real-time. We ran a few experiments on some of our largest tables to understand where errors may be occurring, and `stl_load_errors` quickly became our go-to debugging [tool](https://hackernoon.com/tagged/tool).

```
selectfromorder bydesclimit
```

Some of these issues we’re in translating columns from MySQL types to Redshift types. We were able to resolve a good handful of these issues by adding some logic to account for specific types during the conversion and to account for patterns in our schema, which we were able to match based on column name and type.

```
'md5' inor 'uuid' in
```

Another culprit of errors are newlines present in the data, which causes a line to get split into two (or more) rows which then fail to parse. The solution here was to use a consistent and purposeful delimiter on either side of the equation. From mysql:

```
selectfromINTOBY ','by '"'by '\\'BY '\n'ONON
```

And pairing it with the Redshift query

```
TRUNCATECOPYfromDELIMITER','TRUNCATECOLUMNSEMPTYASNULLACCEPTINVCHARSIGNOREBLANKLINESNULL AS '\\N'MANIFESTREMOVEQUOTESSTATUPDATE ONMAXERRORESCAPE
```

### Dawn of a New Day — The Intern Arrives

Instead of hard-coded schema files, we want to move the configuration files into a persistent storage layer which we planned on calling `dbdb`, or database-database — a moniker we are inheriting from members of our engineering team who worked on a similar system at Square.

We received the feedback to not call it `dbdb` around the same time that Michael Troute joined us for the Summer as a software engineering intern. He identified a need for Plaid to support ad-hoc uploading of CSVs to our Redshift cluster, and we agreed to combine CSV uploads, DBDB, and other planned ETL improvements under the broader umbrella of Data Warehouse Management.

[Getting%20Ramped-Up%20on%20Airflow%20with%20MySQL%20%E2%86%92%20S3%20%E2%86%92%20Red%20fe5c5eac59174ba4ab5b574b8aabfc0c/08Iv1PLLUhgAXF07H](Getting%20Ramped-Up%20on%20Airflow%20with%20MySQL%20%E2%86%92%20S3%20%E2%86%92%20Red%20fe5c5eac59174ba4ab5b574b8aabfc0c/08Iv1PLLUhgAXF07H)

This paid immediate dividends for our development team. When we first started working with Airflow there were a handful of DAGs governed by a pair of configuration files, but the addition of several MySQL databases and an increasing suite of use cases led to the team having to open several pull requests just for configuration changes. Storing the state in the data warehouse manager instead lets us more easily modify the system— automatically adding and removing tables and columns as they get added or dropped from the upstream database and adding custom functionality like setting Redshift sort and distribution keys, and deploying better methodology for our database ingestion.

Some of our tables are billions of rows, and many of these tables are either “append-only” or “sliding-window” updates. For append-only tables the proverbial “low-hanging-fruit” is to only query new rows from the database. For other tables, the rows that are updated are usually created within the past few days, so a mixture of full, partial, and incremental updates will make sense here.

[Getting%20Ramped-Up%20on%20Airflow%20with%20MySQL%20%E2%86%92%20S3%20%E2%86%92%20Red%20fe5c5eac59174ba4ab5b574b8aabfc0c/0fHWtykoaK8rucWuS](Getting%20Ramped-Up%20on%20Airflow%20with%20MySQL%20%E2%86%92%20S3%20%E2%86%92%20Red%20fe5c5eac59174ba4ab5b574b8aabfc0c/0fHWtykoaK8rucWuS)

Iterative loading, easily controlled maintaining state in the Data Warehouse Manager

### Alternative Solutions

We took a foray into using existing solutions that would save us the engineering effort. Our favorite tool out of this investigation was [Matillion](https://www.matillion.com/), and if you’re looking for a drag-n-drop style data pipeline tool, I would definitely check them out. They offer an Amazon Machine Image (AMI) that you can deploy inside of your AWS infrastructure and have great support for these kinds of problems. Ultimately, we identified that our use-case required too much external processing for Matillion to be the right solution for us.

If you’re looking for a cloud provider, we’ve had success using [Stitch Data](https://www.stitchdata.com/) for data processing pipelines, [this post from Amazon](https://aws.amazon.com/blogs/aws/fast-easy-free-sync-rds-to-redshift/) recommends additional vendors, and [Panoply](https://blog.panoply.io/how-to-move-your-mysql-to-amazon-redshift) recommends a similar method using mysqldump.

### Conclusion

Airflow has been a reliable tool for us and is an important part of our in-house ETL efforts. Plaid works with many different data sources, and for non-sensitive datasets + 3rd-party data [Stitch](https://www.stitchdata.com/) and [Segment](https://segment.com/) have been instrumental in building up data workflows. For our data under our on-premise security umbrella, Airflow has shown itself to be reliable, informative, and accessible to new members of the team getting ramped up on data ingestion at Plaid.

Plaid has a blossoming data ecosystem spanning many billions of rows. If you’re an airflow veteran or live and breathe ETL pipelines we’d love to chat! We’d especially love to open-source our efforts: if you like working on these kinds of problems or think this solution could help your own use case, we’d love to get in touch in the comments below.