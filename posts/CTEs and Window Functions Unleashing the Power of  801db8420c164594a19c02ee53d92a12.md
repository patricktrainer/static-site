# CTEs and Window Functions: Unleashing the Power of Redshift

Created: Feb 21, 2020 12:08 PM
URL: https://engineeringblog.yelp.com/2015/01/title-ctes-and-window-functions-unleashing-the-power-of-redshift.html

At Yelp, we’re very big fans of Amazon’s RedShift data warehouse. We have multiple deployments of RedShift with different data sets in use by product management, sales analytics, ads, [SeatMe](https://www.seatme.yelp.com/) and many other teams.

While it minimizes a lot of the work the RedShift team has done to call RedShift a simple fork of Postgres 8.4, RedShift does share a common code ancestry with PG 8.4. This means that much of the advanced query functionality of Postgres is available, which, when combined with the petabyte scale of RedShift, offers some amazingly powerful analytics tools.

Because most of the PG 8.4 query syntax is available, I often find that directly referencing the [Postgres 8.4 documentation](http://www.postgresql.org/docs/8.4/static/sql-select.html) for query syntax is more readable and useful than trying to navigate Amazon’s version of the same documentation.

## CTEs (Common Table Expressions): Scaling Your Queries

When dealing with OLAP (online analytical processing, or warehousing) queries, especially with more snowflake schemas, it’s very common for the number of joins in a query to get large. Snowflake schemas are those where dimension tables are designed to be joined to other dimension tables, which is typical when portions of a transaction schema are mirrored into the data warehouse. RedShift (and Postgres) are well optimized for large numbers of joins, but unfortunately our brains are not.

Correctness of analytics queries is paramount; basing your business decisions on faulty data can be an extremely costly mistake. One of the reasons SQL has gotten a bad reputation for doing analytics work is complexity; a traditional procedural language has functions and procedures that let you encapsulate and compose blocks of logic, while SQL does not.

CTEs (Common Table Expressions) bring this same power of encapsulation and composability to SQL; by allowing you to compose multiple independent queries into a single statement, you can write SQL that is much clearer and easier to verify and debug.

### An Example CTE: Using The WITH Statement

One of the common things we have to do inside the SeatMe codebase is determine when a restaurant’s opening and closing times for various meals occur (internally referred to as scheduled shifts). It’s very common to compute things based on these scheduled times, such as how busy the restaurant is. A (much simplified) version of this query looks like:

The query itself, with its 2 joins, is understandable and independently verifiable. We then use this with a CTE in our analytics to compute things like reservations per shift.

Conceptually you’ve created a temporary table called `scheduled_shifts` with the results of the first query that you can join against in the second query.

One of the benefits of using CTEs when composing queries is that if they are getting re-used frequently, you can create a view over the same statement. If performance of the statement being used in the CTE is a concern and the data can be cached without hurting correctness, you can also trivially create a temporary table with the results of the CTE with only minimal change and very low risk to the overall query correctness.

It does bear saying: CTEs in both RedShift and Postgres represent an optimization barrier. When using a CTE the optimizer is unable to perform optimizations across the query in the body of the CTE and the main query, though it does optimize each of them individually. While this can be an issue, in the real world we’ve found the conceptual benefits greatly outweigh the performance drawbacks.

## Window Functions or “Dang, I didn’t know SQL could do that.”

PostgreSQL Window Functions, which are available in RedShift, are extremely complex and difficult to explain. My goal here is to give a broad overview of the concepts and enough information to encourage people to try them out. Ultimately you’ll need to read and refer to the PostgreSQL documentation on [Window Functions](http://www.postgresql.org/docs/8.4/static/functions-window.html) and [Window Function Calls](http://www.postgresql.org/docs/8.4/static/sql-expressions.html#SYNTAX-WINDOW-FUNCTIONS), along with the [tutorial](http://www.postgresql.org/docs/8.4/static/tutorial-window.html) when using them in your own queries.

Window functions are a special class of analytic functions that are applied to windows of rows. Windows are defined by an `OVER (...)` clause which defines a set of rows related to the current row to which the function applies. While that’s extremely abstract, the diverse functionality available from the different window functions doesn’t really lend itself to a simpler definition.

The two main components of the window are:

- `PARTITION BY` which is the logical analog of `GROUP BY` in a traditional query. Window functions that aggregate will do so across all rows in the partition.
- `ORDER BY` which is required for certain functions that look forward or backward in the window.
- The `FRAME` clause, which is harder to cover, and I’ll not go into in depth. The frame is another logical concept only used by functions that are relative to the frame (like `first_value` / `last_value`)

I think of window functions as falling into two categories:

- Functions that are also available as traditional analytics functions, such as `count`, `sum`, `avg`, etc.
- Functions that are only available when using windows, such as `lead`, `lag`, `ntile`, etc. These expose truly novel functionality unavailable without using windows.

For functions that are also available when using `GROUP BY`, the primary advantage of using them with window functions is it becomes possible to do multiple different grouping operations in a single query. When combined with the power of subqueries and CTEs, this can let you do very powerful business logic all in a single statement.

It would be natural to assume that doing multiple grouping operations in a single query would be just as costly in terms of execution time as doing multiple single operations. In practice, we haven’t seen this to be the case. There is of course a cost, but we typically see it be much smaller than a 100% overhead depending on the query and the grouping.

### Window Function Examples: Using Multiple Traditional Aggregates

The following query illustrates the use of multiple count functions over different partitions to compute the percent of reservations that a given restaurant accounts for by locality (city). The things to note in this query are:

- Use of `DISTINCT`: Since window functions append columns to each row, without a `DISTINCT` operator, the query will give you back 1 row for every row in the join. For this query, this would be 1 row per reservation rather than a row per restaurant and city.
- The two count operations each have a different `PARTITION BY` clause, one counting by restaurant and the other counting by locality.
- The final query, which references the two columns produced by the window function in a CTE and computes a percentage using them.

### Window Function Examples: Using ntile To Compute Percentiles

Frequently, Yelp needs to look at distributions of user activity and compute percentile buckets based on their activity. The query below uses the `ntile` function to augment a per-user count of lifetime review behavior. Things to note about this query:

- `The ntile(100)` is `PARTITION BY signup_country`, so it will compute the percentile per signup country.
- The `ntile(100)` is `ORDER BY review_count`, which means the rows will be bucketed in order of the review_count.
- Each row will get a number from 1-100, that is the logical bucket that the row falls into, added as a new column called `percentile`.

I’ve touched on two of the most powerful features for Redshift analytics, window functions and CTEs, but there’s a lot more functionality in Postgres, much of which is also in RedShift. One of my favorite Postgres sessions is [Postgres: The Bits You Haven’t Found](https://devcenter.heroku.com/articles/postgres-the-bits-you-havent-found-yet), which showed me a whole huge set of Postgres functionality, including first exposing me to window functions.

In addition, brushing up on your [psql chops](http://www.craigkerstiens.com/2013/02/21/more-out-of-psql/) pays dividends over time as you start to become fluid with the advanced functionality in the Postgres CLI. If you write a lot of date based reports, which I suspect we all do, I would also recommend digging into the [date/time functionality](http://www.postgresql.org/docs/8.4/static/functions-datetime.html) (in particular date_trunc). [date_trunc](http://www.postgresql.org/docs/8.4/static/functions-datetime.html#FUNCTIONS-DATETIME-TRUNC) makes doing date based roll ups extremely fast and easy, letting you quickly truncate dates to useful things to months, quarters, weeks, etc.