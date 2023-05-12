# Product Overview – Materialize

Created: Feb 18, 2020 5:46 PM
URL: https://materialize.io/product/

Stream your data. Perform real-time joins. Get instant results.

[Download Materialize](https://materialize.io/download/)

## What is a Streaming Data Warehouse?

All of the interactive queryable capabilities of a traditional SQL data warehouse, but connecting directly to your streaming data sources, and staying up-to-date within milliseconds. ‎‎‏‏‎ ‎

No more compromising between flexibility and speed. Materialize delivers SQL exploration for streaming events and real-time data.

No "inspired by SQL" capabilities or half-broken query languages. Materialize is wire compatible with PostgreSQL.

No more ‘eventual consistency’. Materialize emphasizes the correct answer in real-time - without interference from late-arriving data.

![Product%20Overview%20%E2%80%93%20Materialize%207a2274961f7f4c97bd74302ba150b8cb/product-large.png](Product%20Overview%20%E2%80%93%20Materialize%207a2274961f7f4c97bd74302ba150b8cb/product-large.png)

![Product%20Overview%20%E2%80%93%20Materialize%207a2274961f7f4c97bd74302ba150b8cb/rest-of-SQL-01-1250.png](Product%20Overview%20%E2%80%93%20Materialize%207a2274961f7f4c97bd74302ba150b8cb/rest-of-SQL-01-1250.png)

Many streaming solutions require the denormalization of data in order to maintain low latency - thereby prohibiting any kind of data enrichment like joins.

By contrast, Materialize offers joins in a SQL interface - including complicated multiple-way (e.g. 6-way, 12-way) joins across disparate data sources.

### ...and the rest of SQL, too.

Materialize provides a single element in the most common programming language. Lower the burden on your data platform team and reuse skills from traditional SQL-based data warehouses.

We support the TPC-H benchmark - a standard built for industry-wide relevance, large data volumes, and high query complexity - with incremental updates.

![Product%20Overview%20%E2%80%93%20Materialize%207a2274961f7f4c97bd74302ba150b8cb/SQL-joins-01-1250.png](Product%20Overview%20%E2%80%93%20Materialize%207a2274961f7f4c97bd74302ba150b8cb/SQL-joins-01-1250.png)

![Product%20Overview%20%E2%80%93%20Materialize%207a2274961f7f4c97bd74302ba150b8cb/connect-to-kafka-01-1250.png](Product%20Overview%20%E2%80%93%20Materialize%207a2274961f7f4c97bd74302ba150b8cb/connect-to-kafka-01-1250.png)

### Connects directly to event stream processors

Materialize connects directly to your streaming infrastructure, ingesting streams of data from event stream processors like Kafka. Or connect us directly to your database as a read replica.

Simplify your streaming data architecture. With Materialize, there is no pre-processing of data required to make the system work.

### Combine and analyze real-time and historical data

Want to run queries against both real-time and historical data? Simply connect Materialize to a storage system like Amazon S3 and union both sources together for a full picture of your data.

The potential for these kinds of enriched streams is massive, and we’re excited to see what our customers can do.

![Product%20Overview%20%E2%80%93%20Materialize%207a2274961f7f4c97bd74302ba150b8cb/combine-data-01-1250.png](Product%20Overview%20%E2%80%93%20Materialize%207a2274961f7f4c97bd74302ba150b8cb/combine-data-01-1250.png)

![Product%20Overview%20%E2%80%93%20Materialize%207a2274961f7f4c97bd74302ba150b8cb/postgres-01-1250.png](Product%20Overview%20%E2%80%93%20Materialize%207a2274961f7f4c97bd74302ba150b8cb/postgres-01-1250.png)

### Presents as Postgres downstream

Materialize is wire compatible with PostgreSQL, presenting to downstream tools like any Postgres database, simplifying the development of custom applications and streamlining the process of connecting existing data analysis tools.

Even non-technical users can unlock the most complex real-time queries just using standard BI tooling.

### Build views on views on views - or export back to your event stream processor

Transformations on streaming data can be used to feed into other transformations of that data - say joining several sources, then further querying that information.

Incrementally updating feeds can be directed back into Kafka as a topic for additional applications.

![Product%20Overview%20%E2%80%93%20Materialize%207a2274961f7f4c97bd74302ba150b8cb/views-on-views-01-1250.png](Product%20Overview%20%E2%80%93%20Materialize%207a2274961f7f4c97bd74302ba150b8cb/views-on-views-01-1250.png)

→ Live customer service dashboards → Real-time metrics for Saas apps → Digital media reporting → Real-time risk modeling

→ Real time billing → Live revenue projection → Rapid in-game adjustments → Dynamic audience segmentation

![Product%20Overview%20%E2%80%93%20Materialize%207a2274961f7f4c97bd74302ba150b8cb/read-replica-01-1250.png](Product%20Overview%20%E2%80%93%20Materialize%207a2274961f7f4c97bd74302ba150b8cb/read-replica-01-1250.png)

## Use Materialize as an Optimized Read Replica Database

Traditional read replica databases are optimized for transactional loads – but are usually suboptimal for analytics or visualization. As queries increase, the system can slow down considerably. Using a traditional data warehouse speeds up analytics queries – but on stale data.

Materialize can be used as a highly performant read replica of your relational database – enabling blazing fast analytics queries for data sets both large and small – while staying up-to-date within milliseconds of newly committed transactions.

Materialize can deploy in three ways - as a shared deployment in our multi-tenant cloud, within a customer-specific VPC cloud (managed and owned by Materialize), or within a customer’s public cloud account.

Our system offers high availability via active-active replication. Materialize delivers the output benchmarks of extreme scalability without the performance and expense trade-offs of traditional approaches to scaling.

## Powered by Timely Dataflow

Materialize offers all of the benefits of Timely Dataflow and Differential Dataflow as a managed cloud service. Both systems have been in open-source development for over 4 years and run in production deployments at global scale.

Timely Dataflow is a low-latency cyclical dataflow computational model that excels at delivering high performance, expressive computation, and consistent results.

![Product%20Overview%20%E2%80%93%20Materialize%207a2274961f7f4c97bd74302ba150b8cb/timely-dataflow-01-1250.png](Product%20Overview%20%E2%80%93%20Materialize%207a2274961f7f4c97bd74302ba150b8cb/timely-dataflow-01-1250.png)