# Some SQL Tricks of an Application DBA | Haki Benita

Created: Jul 29, 2020 5:43 PM
Tags: Data, Data engineering, SQL
URL: https://hakibenita.com/sql-tricks-application-dba

When I started my career in development, my first job was a DBA. Back then, before AWS RDS, Azure, Google Cloud and the rest of them cloud services, there were two types of DBAs:

**The Infrastructure DBA** was in charge of setting up the database, configuring the storage and taking care of backups and replication. After setting up the database, the infrastructure DBA would pop up from time to time and do some "instance tuning", things like sizing caches.

**The Application DBA** got a clean database from the infrastructure DBA, and was in charge of schema design: creating tables, indexes, constraints, and tuning SQL. The application DBA was also the one who implemented ETL processes and data migrations. In teams that used stored procedures, the application DBA would maintain those as well.

Application DBAs were usually part of the development team. They would possess deep domain knowledge so normally they would work on just one or two projects. Infrastructure DBAs would usually be part of some IT team, and would work on many projects simultaneously.

**I'm an Application DBA**

I never had any desire to fiddle with backups or tune storage (I'm sure it's fascinating!). Until this day I like to say I'm a DBA that knows how to develop applications, and not a developer that knows his way around the database.

**In this article I share some non-trivial tips about database development I gathered along the way.**

![Some%20SQL%20Tricks%20of%20an%20Application%20DBA%20Haki%20Benita%20d12ecc59d61444cb8b1f2617afa36718/00-sql-tricks-dba.jpg](Some%20SQL%20Tricks%20of%20an%20Application%20DBA%20Haki%20Benita%20d12ecc59d61444cb8b1f2617afa36718/00-sql-tricks-dba.jpg)

Be that guy...Image by [CommitStrip](https://www.commitstrip.com/en/2014/08/01/when-i-help-a-rookie-coder-fix-his-queries)

`UPDATE` is a relatively expensive operation. To speed up an `UPDATE` command it's best to make sure you only update what needs updating.

Take this query for example that normalizes an email column:

```
db=# UPDATE users SET email = lower(email);
UPDATE 1010000
Time: 1583.935 ms (00:01.584)

```

Looks innocent, right? the query updated emails of 1,010,000 users. But, did all rows really needed to update?

```
db=# UPDATE users SET email = lower(email)
db-# WHERE email != lower(email);
UPDATE 10000
Time: 299.470 ms

```

Only 10,000 rows needed to update. By reducing the amount of affected rows, the execution time went down from 1.5 seconds to just less than 300ms. Updating fewer rows also saves the database maintenance later on.

This type of large updates are very common in data migration scripts. So the next time you write a migration script, make sure to only update what needs updating.

Constraints are an important part of relational databases: they keep the data consistent and reliable. Their benefits come at a cost though, and it's most noticeable when loading or updating a lot of rows.

To demonstrate, set up a small schema for a store:

```
DROP TABLE IF EXISTS product CASCADE;
CREATE TABLE product (
    id serial PRIMARY KEY,
    name TEXT NOT NULL,
    price INT NOT NULL
);
INSERT INTO product (name, price)
    SELECT random()::text, (random() * 1000)::int
    FROM generate_series(0, 10000);

DROP TABLE IF EXISTS customer CASCADE;
CREATE TABLE customer (
    id serial PRIMARY KEY,
    name TEXT NOT NULL
);
INSERT INTO customer (name)
    SELECT random()::text
    FROM generate_series(0, 100000);

DROP TABLE IF EXISTS sale;
CREATE TABLE sale (
    id serial PRIMARY KEY,
    created timestamptz NOT NULL,
    product_id int NOT NULL,
    customer_id int NOT NULL
);

```

The schema defines different types of constraints such as "not null" and unique constraints.

To set a baseline, start by adding foreign keys to the `sale` table, and then load some data into it:

```
db=# ALTER TABLE sale ADD CONSTRAINT sale_product_fk
db-# FOREIGN KEY (product_id) REFERENCES product(id);
ALTER TABLE
Time: 18.413 ms

db=# ALTER TABLE sale ADD CONSTRAINT sale_customer_fk
db-# FOREIGN KEY (customer_id) REFERENCES customer(id);
ALTER TABLE
Time: 5.464 ms

db=# CREATE INDEX sale_created_ix ON sale(created);
CREATE INDEX
Time: 12.605 ms

db=# INSERT INTO SALE (created, product_id, customer_id)
db-# SELECT
db-#    now() - interval '1 hour' * random() * 1000,
db-#    (random() * 10000)::int + 1,
db-#    (random() * 100000)::int + 1
db-# FROM generate_series(1, 1000000);
INSERT 0 1000000
Time: 15410.234 ms (00:15.410)

```

After defining constraints and indexes, loading a million rows to the table took ~15.4s.

Next, try to load the data into the table first, and only then add constraints and indexes:

Loading data into a table without indexes and constraints was much faster, 2.27s compared to 15.4s before. Creating the indexes and constraints after the data was loaded into the table took a bit longer, but overall the entire process was much faster, 3.1s compared to 15.4s.

Unfortunately, for indexes PostgreSQL does not provide an easy way of doing this other than dropping and re-creating the indexes. In other databases such as Oracle, you can [disable and enable indexes](https://docs.oracle.com/en/database/oracle/oracle-database/19/sqlrf/ALTER-INDEX.html#GUID-D8F648E7-8C07-4C89-BB71-862512536558) without having to re-create them.

When you modify data in PostgreSQL, the changes are written to the [write ahead log (WAL)](https://www.postgresql.org/docs/current/wal-intro.html). The WAL is used to maintain integrity, to fast forward the database during recovery and to maintain replication.

Writing to the WAL is often needed, but there are some circumstances where you might be willing to give up some of its uses to make things a bit faster. One example is intermediate tables.

Intermediate tables are disposable tables that stores temporary data used to implement some process. For example, a very common pattern in ETL processes is to load data from a CSV file to an intermediate table, clean the data, and then load it to the target table. In this use-case, the intermediate table is disposable and there is no use for it in backups or replicas.

Intermediate tables that don't need to be restored in case of disaster, and are not needed in replicas, can be set as [UNLOGGED](https://www.postgresql.org/docs/current/sql-createtable.html#SQL-CREATETABLE-UNLOGGED):

**BEWARE**: Before using `UNLOGGED` make sure you understand its full implications.

Say you have a users table, and you find that you have some duplicates in the table:

The user *haki benita* registered twice, once with the email `ME@hakibenita.com` and again with `me@hakibenita.com`. Because we didn't normalize the emails when we inserted them into the table, we now have to deal with duplication.

To consolidate the duplicate users, we want to:

1. Identify duplicate users by lower case email
2. Update orders to reference one of the duplicate users
3. Remove the duplicate users from the users table

One way to consolidate duplicate users is to use an intermediate table:

The intermediate table holds a mapping of duplicate users. For each user that appears more than once with the same normalized email address, we define the user with the min ID as the user we convert all duplicates to. The other users are kept in an array column, and all the references to these users will be updated.

Using the intermediate table, we update references of duplicate users in the `orders` table:

Now that there are no more references, we can safely delete the duplicate users from the `users` table:

Notice that we used the function `[unnest](https://www.postgresql.org/docs/current/functions-array.html#ARRAY-FUNCTIONS-TABLE)` to "transpose" the array, that is, turn each array element into a row.

This is the result:

Nice, all occurrences of user 3 (ME@hakibenita.com) are converted to user 2 (me@hakibenita.com).

We can also verify that the duplicate users were deleted from the `users` table:

Now we can get rid of the intermediate table:

This is fine, but very long and needs cleaning up! Is there a better way?

**Using Common Table Expressions (CTE)**

Using [Common Table Expressions](https://www.postgresql.org/docs/current/queries-with.html), also known as the `WITH` clause, we can perform the entire process with just one SQL statement:

Instead of creating the intermediate table, we create a common table expression and reuse it multiple times.

**Returning Results From CTE**

A nice feature of executing DML inside a `WITH` clause, is that you can return data from it using the `[RETURNING` keyword](https://www.postgresql.org/docs/current/dml-returning.html). For example, let's report the number of updated and deleted rows:

This is the result:

The main appeal of this approach is that the entire process is executed in a single command, so no need to manage a transaction or worry about cleaning up the intermediate table if the process fails.

Say you have a registration process where users sign up with an email address. To activate the account, they have to verify their email. Your table can look like this:

Most of your users are good citizens, they sign up with a valid email and immediately activate the account. Let's populate the table with user data, where roughly 90% of the users are activated:

To query for activated and unactivated users, you might be tempted to create an index on the column `activated`:

When you try to query *unactivated users*, the database is using the index:

The database estimated that the filter will result in 102,567 which are roughly 10% of the table. This is consistent with the data we populated, so the database has a good sense of the data.

However, when you try to query for *activated users* you find that the database decided *not to use the index*:

Many developers are often baffled when they the database is not using an index. One way of explaining why an index is not always the best choice is this: **if you had to read the entire table, would you use the index?**

The answer is probably no, because why would you? Reading from disk is expensive and you want to read as little as possible. If for example, a table is 10MB and the index is 1MB, to read the entire table you would have to read 10MB from disk. To read the table using the index you would have to read 11MB from disk. This is wasteful.

With this understanding, let's have a look at the statistics PostgreSQL gather on the table:

When PostgreSQL analyzed the table it found that the column `activated` has two distinct values. The value `t` in the `most_common_vals` column corresponds to the frequency `0.89743334` in the column `most_common_freqs`, and the value `f` corresponds to the frequency `0.10256667`. This means that after analyzing the table, the database estimates that 89.74% of the table are activated users, and the rest 10.26% are unactivated users.

With these stats, PostgreSQL decided it's best to scan the entire table if it expects 90% of the rows to satisfy the condition. The threshold after which the database may decide to use or not to use the index depends on many factors, and there is no rule of thumb you can use.

In the previous section we created an index on a boolean column where ~90% of the of the values were true (activated user). When we tried to query for active users, the database did not use the index. However, when we queried unactivated users the database did use the index.

This brings us to the next question.... if the database is not going to use the index to filter active users, why should we index them in the first place?

Before we answer this question let's look at how much the full index on the `activated` column weighs:

The index is 21MB. Just for reference, the `users` table is 65MB. This means the index weighs ~32% the size of the table. We also know that ~90% of the index is likely not going to be used.

In PostgreSQL, there is a way to create an index on only a part of the table, using whats called a [partial index](https://www.postgresql.org/docs/current/indexes-partial.html):

Using a `WHERE` clause, we restrict the rows indexed by the index. Let's first make sure it works:

Amazing, the database was smart enough to understand that the predicate we used in the query can be satisfied by the partial index.

There is another benefit to using partial indexes:

The partial index weighs only 2.2MB. The full index on the column weighed 21MB. The partial index is exactly 10% the size of the full index, which matches the ratio of inactive users in the table.

This is one of the things I comment most about in code reviews. It's not as intuitive as the other tips and it can have a huge impact on performance.

Say you have a large sales fact table:

Every night, during some ETL process, you load data into the table:

To fake a loading process we used random data. We inserted 100K rows with random username, and sale dates from 2020-01-01 to two years forward.

The table is used mostly to produce summary sales reports. Most reports filter by date to get the sales at a specific period. To speed up range scans you create an index on `sold_at`:

Let's look at the execution plan of a query to fetch all sales made in June 2020:

After executing the query several times to warm up the cache, the timing settled at ~6ms.

**Bitmap Scan**

Looking at the execution plan, we can see that the database used a bitmap scan. A bitmap scan works in two stages:

- `Bitmap Index Scan`: Go through the entire index `sale_fact_sold_at_ix` and map all the table pages that contain relevant rows.
- `Bitmap Heap Scan`: Read the pages that contain relevant rows, and find the rows inside these pages that satisfy the condition.

Pages can contain multiple rows. The first step uses the index to find *pages*. The second step check for *rows* inside these pages, hence the "Recheck Cond" operation in the execution plan.

At this point many DBAs and developers will call it a day and move on to the next query. BUT, there's a way to make this query better.

**Index Scan**

To make things better, we'll make a small change in how we load the data.

This time, we loaded the data sorted by the `sold_at`.

Let's see what the execution plan for the exact same query looks like now:

After running the query several times we get a stable timing at round 2.3ms. Compared to the previous query that took ~6ms, we get a consistent saving of ~60%.

Another thing we can see right away, is that the database did not use a bitmap scan this time, but a "regular" index scan. Why is that?

**Correlation**

When the database is analyzing a table it collects all sort of statistics. One of those statistics is **[correlation](https://www.postgresql.org/docs/current/view-pg-stats.html)**:

> Statistical correlation between physical row ordering and logical ordering of the column values. This ranges from -1 to +1. When the value is near -1 or +1, an index scan on the column will be estimated to be cheaper than when it is near zero, due to reduction of random access to the disk.

As the official documentation explains, the correlation measures how "sorted" values of a specific column are on disk.

When the correlation is 1, or close to 1, it means the pages in the tables are stored on disk in roughly the same order as the rows in the table. This is actually very common. For example, auto incrementing ID's will usually have a correlation close to 1. Date and timestamp columns that keeps track of when rows were created will also usually have a correlation close to 1.

When the correlation is -1, the pages of the table are sorted in reverse order relative to the column.

When the correlation is close to 0, it mean the values in the column have no or very little correlation to how the pages of the table are stored.

Going back to our `sale_fact` table, when we loaded the data into the table without sorting it first, these were the correlations:

The auto generated column `id` has a correlation of 1. The `sold_at` column has a very low correlation: consecutive values are scattered across the entire table.

When we loaded sorted data into the table, these were the correlations calculated by the database:

The correlation for `sold_at` is now 1.

So why did the database use a bitmap scan when the correlation was low, and an index scan when the correlation was close to 1?

- When the correlation was 1, the database estimated that rows in the requested range are likely to be in consecutive pages. In this case, an index scan is likely to read very few pages.
- When the correlation was close to 0, the database estimated that rows in the requested range are likely to be scattered across the entire table. In this case, it makes sense to use a bitmap scan to map the table pages in which rows exist, and only then fetch them and apply the condition.

The next time you load data into a table, think about how the data is going to be queried, and make sure you sort it in a way that indexes used for range scan can benefit from.

**`CLUSTER` Command**

Another way of "sorting a table on disk" by a specific index is to use the `[CLUSTER` command](https://www.postgresql.org/docs/current/sql-cluster.html).

For example:

We loaded data into the table in random order and as a result the correlation of `sold_at` is close to zero.

To "rearrange" the table by `sold_at`, we used the `CLUSTER` command to sort the table on disk according to the index `sale_fact_sold_at_ix`:

After the table was clustered we can see that the correlation for `sold_at` is 1.

Some things to note about the `CLUSTER` command:

- Clustering the table by a specific column may affect the correlation of other column. See for example the correlation of the column `id` after we clustered the table by `sold_at`.
- `CLUSTER` is a heavy, blocking operation, so make sure you don't execute it on a live table.

For these two reason it's best to insert the data sorted and not rely on `CLUSTER`.

When talking about indexes, most developers will think about B-Tree indexes. But, PostgreSQL provides other types of indexes such as [BRIN](https://www.postgresql.org/docs/current/brin.html):

> BRIN is designed for handling very large tables in which certain columns have some natural correlation with their physical location within the table

BRIN stands for Block Range Index. According to the documentation, a BRIN index works best for columns with high correlation. As we've already seen in previous sections, some fields such as auto incrementing IDs and timestamps are naturally correlated with the physical structure of the table, hence they are good candidates for a BRIN index.

Under some circumstances, a BRIN index can provide a better "value for money" in terms of size and performance compared to a similar B-Tree index.

A BRIN index works by keeping the range of values within a number of adjacent pages in the table. Say we have these values in a column, each is single table page:

A BRIN index works on ranges of adjacent pages in the table. If the number of adjacent pages is set to 3, the index will divide the table into the following ranges:

For each range, the BRIN index **keeps the minimum and maximum value**:

Using the index above, try to search for the value 5:

- `[1–3]` - Definitely not here
- `[4–6]` - Might be here
- `[7–9]` - Definitely not here

Using the BRIN index we managed to limit our search to blocks 4–6.

Let's take another example, this time the values in the column will have a correlation close to zero, meaning they are *not* sorted:

Indexing 3 adjacent blocks produces the following ranges:

Let's try to search for the value 5:

- `[2–9]` - Might be here
- `[1–7]` - Might be here
- `[3–8]` - Might be here

In this case the index is not limiting the search *at all*, hence it is useless.

**Understanding `pages_per_range`**

The number of adjacent pages is determined by the parameter `pages_per_range`. The number of pages per range effects the size and accuracy of the BRIN index:

- A large `pages_per_range` will produce a small and less accurate index
- A small `pages_per_range` will produce a bigger and more accurate index

The default `pages_per_range` is 128.

To demonstrate, let's create a BRIN index on ranges of 2 adjacent pages and search for the value 5:

- `[1–2]` - Definitely not here
- `[3–4]` - Definitely not here
- `[5–6]` - Might be here
- `[7–8]` - Definitely not here
- `[9]` - Definitely not here

Using the index with 2 pages per range we were able to limit the search to blocks 5 and 6. When the range was 3 pages, the index limited the search to blocks 4,5 and 6.

Another difference between the two indexes is that when the range was 3 we only had to keep 3 ranges. When the range was 2 we had to keep 5 ranges so the index was bigger.

**Creating a BRIN Index**

Using the `sales_fact` from before, let's create a BRIN index on the column `sold_at`:

This creates a BRIN index with the default `pages_per_range = 128`.

Let's try to query for a range of sale dates:

The database used our BRIN index to get a range of sale dates, but that's not the interesting part...

**Optimizing `pages_per_range`**

According to the execution plan, the database removed 23,130 rows from the pages it found using the index. This may indicate that the range we set for the index it too large for this particular query. Let's try to create an index with less pages per range:

With 64 pages per range the database removed less rows from the pages it found using the the index, only 9,434 were removed compared with 23,130 when the the range was 128 pages. This means the database had to do less IO and the query was slightly faster, ~5.5ms compared to ~8.9ms.

Testing the index with different values for `pages_per_range` produced the following results:

We can see that as we decrease `pages_per_range`, the index is more accurate and less rows are removed from the pages found using the index.

Note that we optimized the query for a very specific query. This is fine for demonstration purposes, but in real life it's best to use values that meet the needs of most queries.

**Evaluating Index Size**

Another big selling point for BRIN indexes is their size. In previous sections we created a B-Tree index on the `sold_at` field. The size of the index was 2224kB. The size a BRIN index with `pages_per_range=128` is only 48kb. That's 46 times smaller than the B-Tree index.

The size of a BRIN index is also affected by `pages_per_range`. For example, a BRIN index with `pages_per_range=2` weighs 56kb, which is only slightly bigger than 48kb.

PostgreSQL has a nice feature called [transactional DDL](https://wiki.postgresql.org/wiki/Transactional_DDL_in_PostgreSQL:_A_Competitive_Analysis#Transactional_DDL). After years of using Oracle, I got used to DDL commands such as `CREATE`, `DROP` and `ALTER` ending a transaction. However, in PostgreSQL you can perform DDL commands inside a transaction, and changes will take effect only when the transaction is committed.

As I [recently discovered](https://twitter.com/be_haki/status/1282585977668751360?s=20), using transactional DDL you can make indexes invisible! This comes in handy when you want to see what an execution plan looks like without some index.

For example, in the `sale_fact` table from the previous section we created an index on `sold_at`. The execution plan for fetching sales made in July looked like this:

To see what the execution plan would be if the index `sale_fact_sold_at_ix` did not exist, we can drop the index inside a transaction and immediately rollback:

We first start a transaction using `BEGIN`. Then we drop the index and generate an execution plan. Notice that the execution plan now uses a full table scan, as if the index does not exist. At this point the transaction is still in progress, so the index is not dropped yet. To finish the transaction without dropping the index we rollback the transaction using the `ROLLBACK` command.

Now, make sure the index still exists:

Other database that don't support transactional DDL provide other ways to achieve the same goal. For example, Oracle let's you mark an index as [invisible](https://docs.oracle.com/cd/B28359_01/server.111/b28310/indexes003.htm#ADMIN12317), which will cause the optimizer to ignore it.

**CAUTION**: Dropping an index inside a transaction will lock out concurrent selects, inserts, updates, and deletes on the table while the transaction is active. Use with caution in test environments, and avoid on production databases.

It's a known fact among investors that weird things can happen when a stock's price reaches a nice round number such as 10$, 100$, 1000$. As [the following article](https://www.investopedia.com/trading/support-and-resistance-basics/#mntl-sc-block_1-0-38) explains:

> [...] asset's price may have a difficult time moving beyond a round number, such as $50 or $100 per share. Most inexperienced traders tend to buy or sell assets when the price is at a whole number because they are more likely to feel that a stock is fairly valued at such levels.

Developers in this sense are not all that different than the investors. When they need to schedule a long running process, they will usually schedule it at a round hour.

This tendency to schedule tasks at round hours can cause some unusual loads during these times. So, if you need to schedule some long running process, you have a better chance of finding a system at rest if you schedule at another time.

Another good idea is to apply a random delay to the task's schedule, so it doesn't run at the same time every time. This way, even if another task is scheduled to run at the same time, it won't be a big problem. If you use `systemd` timer units to schedule your tasks, you can use the [RandomizedDelaySec](https://www.freedesktop.org/software/systemd/man/systemd.timer.html#RandomizedDelaySec=) option for this.

This article covers some trivial and non-trivial tips from my own experience. Some of these tips are easy to implement, and some require a deeper understanding of how the database works. Databases are the backbone of most modern systems, so taking some time to understand how they work is a good investment for any developer!