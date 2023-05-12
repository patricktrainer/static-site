# Materialize – The Streaming Data Warehouse

Created: Feb 18, 2020 5:46 PM
URL: https://materialize.io/

## Building streaming data architecture can be as simple as writing SQL.

Materialize easily processes complex analytics over streaming datasets – offering the power and flexibility of a SQL data warehouse for the world of real-time data.

![Materialize%20%E2%80%93%20The%20Streaming%20Data%20Warehouse%2042c0148e61144161b240e34a407c7121/home-large.png](Materialize%20%E2%80%93%20The%20Streaming%20Data%20Warehouse%2042c0148e61144161b240e34a407c7121/home-large.png)

Materialize is the only technology that can enable engineers to completely develop for streaming data in a powerful declarative language – PostgreSQL – instead of building microservices.

Materialize empowers anyone within a company to discover insights from real-time data, identify problems immediately, and take action in critical moments.

Materialize connects directly to event stream processors (like Kafka) and incrementally updates computations within milliseconds.

Other systems place the burden on you to make their systems work. Materialize can manage your data as it exists - without any preprocessing required.

No "inspired by SQL" half-broken query languages. Materialize supports PostgreSQL. Use the Postgres CLI or your favorite database adapter.

![Materialize%20%E2%80%93%20The%20Streaming%20Data%20Warehouse%2042c0148e61144161b240e34a407c7121/SQL-01-1250.png](Materialize%20%E2%80%93%20The%20Streaming%20Data%20Warehouse%2042c0148e61144161b240e34a407c7121/SQL-01-1250.png)

Materialize is the first and only streaming system capable of running the TPC-H decision support benchmark – a set of criteria originally developed for the world of batch data warehouses.

This standard includes support for complex joins – including complicated multiple-way joins across disparate data sources – previously unavailable in the world of streaming.

## End the Microservice Morass

A common approach towards building streaming data architecture is to develop a series of custom microservices – which are often time-intensive, complicated, and ultimately brittle.

With Materialize, data engineering teams can move away from the endless development of microservices – and replace thousands of lines of Java with a few lines of SQL.

![Materialize%20%E2%80%93%20The%20Streaming%20Data%20Warehouse%2042c0148e61144161b240e34a407c7121/microservices-01-1250.png](Materialize%20%E2%80%93%20The%20Streaming%20Data%20Warehouse%2042c0148e61144161b240e34a407c7121/microservices-01-1250.png)

![Materialize%20%E2%80%93%20The%20Streaming%20Data%20Warehouse%2042c0148e61144161b240e34a407c7121/timely-dataflow-01-1250.png](Materialize%20%E2%80%93%20The%20Streaming%20Data%20Warehouse%2042c0148e61144161b240e34a407c7121/timely-dataflow-01-1250.png)

## Powered by Timely Dataflow

Materialize offers all of the benefits of Timely Dataflow and Differential Dataflow, accessible via the familiar and accessible PostgreSQL. Both systems have been in open-source development for over 4 years and run in production deployments at global scale.

Timely Dataflow is a low-latency cyclical dataflow computational model that excels at delivering high performance, expressive computation, and consistent results.