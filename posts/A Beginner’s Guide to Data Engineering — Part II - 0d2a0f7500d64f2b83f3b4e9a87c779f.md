# A Beginner’s Guide to Data Engineering — Part II - Robert Chang - Medium

Created: Feb 21, 2020 12:09 PM
URL: https://medium.com/@rchang/a-beginners-guide-to-data-engineering-part-ii-47c4e7cbda71

![1*BC9-kpfjCPtY-w-GOjPBDA.png](A%20Beginner%E2%80%99s%20Guide%20to%20Data%20Engineering%20%E2%80%94%20Part%20II%20-%200d2a0f7500d64f2b83f3b4e9a87c779f/1BC9-kpfjCPtY-w-GOjPBDA.png)

# Recapitulation

In **[A Beginner’s Guide to Data Engineering** — **Part I](https://medium.com/@rchang/a-beginners-guide-to-data-engineering-part-i-4227c5c457d7),** I explained that an organization’s analytics capability is built layers upon layers. From collecting raw data and building data warehouses to applying Machine Learning, we saw why data engineering plays a critical role in all of these areas.

One of any data engineer’s most highly sought-after skills is the ability to design, build, and maintain data warehouses. I defined what data warehousing is and discussed its three common building blocks — **E**xtract, **T**ransform, and **L**oad, where the name ETL comes from.

For those who are new to ETL processes, I introduced a few popular open source frameworks built by companies like LinkedIn, Pinterest, Spotify, and highlight Airbnb’s own open-sourced tool Airflow. Finally, I argued that data scientist can learn data engineering much more effectively with the SQL-based ETL paradigm.

# Part II Overview

The discussion in part I was somewhat high level. In Part II (this post), I will share more technical details on how to build good data pipelines and highlight ETL best practices. Primarily, I will use Python, Airflow, and SQL for our discussion.

First, I will introduce the concept of **Data Modeling**, a design process where one carefully defines table schemas and data relations to capture business metrics and dimensions. We will learn **Data Partitioning**, a practice that enables more efficient querying and data backfilling. After this section, readers will understand the basics of data warehouse and pipeline design.

In later sections, I will dissect the anatomy of an **Airflow job.** Readers will learn how to use sensors, operators, and transfers to operationalize the concepts of extraction, transformation, and loading. We will highlight **ETL best practices**, drawing from real life examples such as Airbnb, Stitch Fix, Zymergen, and more.

By the end of this post, readers will appreciate the versatility of Airflow and the concept of *[configuration as code](https://airflow.apache.org/#principles)*. We will see, in fact, that Airflow has many of these best practices already built in.

When a user interacts with a product like Medium, her information, such as her avatar, saved posts, and number of views are all captured by the system. In order to serve them accurately and on time to users, it is critical to optimize the production databases for *online transaction processing* (OLTP for short).

When it comes to building an *online analytical processing* system (OLAP for short), the objective is rather different. The designer need to focus on insight generation, meaning analytical reasoning can be translated into queries easily and statistics can be computed efficiently. This analytics-first approach often involves a design process called **data modeling.**

## Data Modeling, Normalization, and Star Schema

To give an example of the design decisions involved, we often need to decide the extent to which tables should be **[normalized](https://en.wikipedia.org/wiki/Database_normalization)**. Generally speaking, normalized tables have simpler schemas, more standardized data, and carry less redundancy. However, a proliferation of smaller tables also means that tracking data relations requires more diligence, querying patterns become more complex (more `JOINs`), and there are more ETL pipelines to maintain.

On the other hand, it is often much easier to query from a denormalized table (aka a wide table), because all of the metrics and dimensions are already pre-joined. Given their larger sizes, however, data processing for wide tables is slower and involves more upstream dependencies. This makes maintenance of ETL pipelines more difficult because the unit of work is not as modular.

Among the many design patterns that try to balance this trade-off, one of the most commonly-used patterns, and the one we use at [Airbnb](https://ieondemand.com/presentations/building-airbnb-s-data-culture-insights-from-5-years-of-hypergrowth?_ga=2.230925083.5245429.1516779379-1586560381.1516779379), is called **[star schema](https://en.wikipedia.org/wiki/Star_schema)**. The name arose because tables organized in star schema can be visualized with a star-like pattern. This design focuses on building normalized tables, specifically fact and dimension tables. When needed, denormalized tables can be built from these smaller normalized tables. This design strives for a balance between ETL maintainability and ease of analytics.

The star schema organized table in a star-like pattern, with a fact table at the center, surrounded by dim tables

## **Fact & Dimension Tables**

To understand how to build denormalized tables from fact tables and dimension tables, we need to discuss their respective roles in more detail:

- **Fact tables** typically contain point-in-time transactional data. Each row in the table can be extremely simple and is often represented as a unit of transaction. Because of their simplicity, they are often the source of truth tables from which business metrics are derived. For example, at Airbnb, we have various fact tables that track transaction-like events such as bookings, reservations, alterations, cancellations, and more.
- **Dimension tables** typically contain slowly changing attributes of specific entities, and attributes sometimes can be organized in a hierarchical structure. These attributes are often called “dimensions”, and can be joined with the fact tables, as long as there is a foreign key available in the fact table. At Airbnb, we built various dimension tables such as users, listings, and markets that help us to slice and dice our data.

Below is a simple example of how fact tables and dimension tables (both are normalized tables) can be joined together to answer basic analytics question such as how many bookings occurred in the past week in each market. Shrewd users can also imagine that if additional metrics `m_a, m_b, m_c` and dimensions `dim_x, dim_y, dim_z` are projected in the final `SELECT` clause, a denormalized table can be easily built from these normalized tables.

Normalized tables can be used to answer ad-hoc questions or to build denormalized tables