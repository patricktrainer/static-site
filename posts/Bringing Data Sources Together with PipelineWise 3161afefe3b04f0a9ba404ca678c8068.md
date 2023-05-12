# Bringing Data Sources Together with PipelineWise

Created: Dec 5, 2019 2:04 PM
Tags: Data
URL: [https://tech.transferwise.com/bringing-data-sources-together-with-pipelinewise/?utm_campaign=Up%20%26%20Running%20Weekly&utm_medium=email&utm_source=Revue%20newsletter](https://tech.transferwise.com/bringing-data-sources-together-with-pipelinewise/?utm_campaign=Up%20%26%20Running%20Weekly&utm_medium=email&utm_source=Revue%20newsletter)

TransferWise is open sourcing it’s data replication framework. [PipelineWise](https://transferwise.github.io/pipelinewise/) is a Data Pipeline Framework using the [Singer.io](https://www.singer.io/) specification to replicate data from various sources to various destinations.

![Bringing%20Data%20Sources%20Together%20with%20PipelineWise%203161afefe3b04f0a9ba404ca678c8068/pipelinewise-diagram-circle-bold.png](Bringing%20Data%20Sources%20Together%20with%20PipelineWise%203161afefe3b04f0a9ba404ca678c8068/pipelinewise-diagram-circle-bold.png)

Like many companies, the first technology stack at TransferWise was a web page with a single back-end database. But even from the earliest days, there’s been a strong focus on measurable metrics and data-driven decision making across the whole organisation. As we grew and the product became more advanced, it became obvious that coping with our growth would require a shift towards [microservices architecture](https://tech.transferwise.com/good-size-for-a-microservice/).

This solved many scaling issues, but also created new challenges for anybody needing to analyse data or even create a simple report. They’d now have to connect to hundreds of data stores. Furthermore, due to our autonomous nature at TransferWise, development teams are free to choose any type of data store to use. All this combined to created a complicated and impractical analytics situation.

# Defining the Requirements

The tool had to be able to replicate hundreds of data sources into a centralised analytics data store where data analysts can do further transformations and can get real insights from data.

The following minimal conditions had to be met:

- **Compatibility** with various data sources and analytics data stores as target
- **Change Data Capture** ([CDC](https://en.wikipedia.org/wiki/Change_data_capture)) mechanism wherever it’s possible to keep the lag as low as possible
- Maximum **security** and self hosted solution with the capability to obfuscate and mask PII and sensitive data at load time
- Apply **schema changes** automatically
- **Scalability**
- Avoiding vendor lock-in; accessing the source code to develop new features and fix issues quickly
- Keeping configuration as **code**

Our first approach was to look for a data transportation product that could satisfy our known use cases and also pass the rigorous requirements defined by our security team. We looked at traditional ETL tools, commercial replication tools and Kafka streaming ETL.

**Traditional ETL tools** didn’t work for us because they typically did not support CDC and automatic schema changes very well. TransferWise already had dozens of databases that kept changing every week and maintaining complex ETL jobs was not realistic.

Some third party tools offered interesting features, however data had to be sent to external servers, which adds additional complexity from compliance and security perspective. TransferWise as a financial services company deals with very sensitive data and thus, in order to move foward with a solution fast, we had to opt for a selfhosted solution.

We found **Kafka Streaming ETL** very promising and that looks like the definite solution for the company's high demand for real-time analytics requirement, but we had some difficulties at the time. The JDBC sink connector wasn't performing well with some columnar analytical data stores like AWS Redshift or Snowflake, traditional key based incremental load or full table snapshots were not trivial, the required infrastructure was not ready, and we had to come up with something quickly. Despite this, we still see great potential in streaming technology in the ETL era as well and currently we're working on the implementation of that with a bigger team of data engineers. We're sure it will enable further capabilites like real-time reporting, unlocks more ML models, A/B/multivariate testing, real-time anomaly detection and a lot more.

# The Result

After several months and dozens of vendors, we re-focussed on improving our internally developed tools.

Staying true to our autonomous philosophy we created a team responsible for every aspect of extracting the data from a wide variety of sources, and transport it in a convenient, secure, auditable and timely manner to a central analytic data store. Soon we found the [Singer specification](https://github.com/singer-io/getting-started/blob/master/docs/SPEC.md), created by Stitch and realised that by building on their great work, we could get to a working solution much quicker.

# Team Effort and Running on Production

[PipelineWise](https://transferwise.github.io/pipelinewise/) was created by our Analytics Platform team in close cooperation with our Data Analysts, and some of the product teams as the main consumers of the data. The project took several months to develop and was initially started as an experiment. It's proven to be successful and was rolled out in multiple stages over the last few months.

PipelineWise now meets all the above initial requirements and is used to replicate **hundreds of GB** of data every day from **120 microservices**, **1500+ tables** and a bunch of external tools into our *Snowflake* data warehouse, with only **minutes of lag**.

![Bringing%20Data%20Sources%20Together%20with%20PipelineWise%203161afefe3b04f0a9ba404ca678c8068/pipelinewise-monitoring-grafana.png](Bringing%20Data%20Sources%20Together%20with%20PipelineWise%203161afefe3b04f0a9ba404ca678c8068/pipelinewise-monitoring-grafana.png)

*Monitoring with [Grafana](https://grafana.com/): Replicating 120 data sources, 1500+ tables into Snowflake with PipelineWise on 3 nodes of c5.2xlarge EC2 instances*

# Limitations

Like any other tools PipelineWise also has limitations:

- **Not Real-Time**: The currently supported target connectors are micro-batch oriented. For example data has to be loaded from S3 via the `COPY` command into *Snowflake* or *Amazon Redshift* because individual `INSERT` statements are not efficient. Creating these batches adds an extra layer to the process and replication cannot be realtime. The realistic **replication lag** from source to target **is between 5 and 30 minutes** depending on the source of data. If you need real real-time data then give a try to Stream Processing with Kafka and don't use columnar stores.
- **Very active transactional tables**: PipelineWise is trying to do parallel processing wherever it's possible. Micro-batches are created in parallel as well, one batch for each table, but currently it can't create one individual batch in parallel. This means that replicating extremely large tables with millions of only `UPDATES` and `DELETES` can be slow when [CDC](https://en.wikipedia.org/wiki/Change_data_capture) replication method is enabled. Currently the preferred method is not using CDC for these type of tables. In this case [Key Based Incremental Replication Method](https://transferwise.github.io/pipelinewise/concept/replication_methods.html#incremental) is faster and still reliable as there are no deleted rows in source.

# Open-Sourcing the Project

TransferWise is ever evolving and the PipelineWise project is likely to evolve for some time to come, but we tentatively feel it’s mature enough to release back to the open-source community. Our hope is that others might benefit from and contribute towards the project, and possibly open up new and exciting ways of analysing data.

For detailed information on PipelineWise features and architecture, check out the documentation on [https://transferwise.github.io/pipelinewise/](https://transferwise.github.io/pipelinewise/).