# DISTINCT ON: The confusing, unique and useful feature in Postgres - Blog by Yogesh Chauhan

Created: Mar 21, 2020 10:04 AM
URL: https://www.yogeshchauhan.com/167/postgres/the-confusing-unique-and-useful-feature-in-postgres-distinct-on

We saw how DISTINCT works at the end of this post: [Select Statement In Postgres With Examples](https://www.yogeshchauhan.com/165/postgres/select-statement-in-postgres-with-examples)

Let's explore it further.

When I saw DISTINCT ON, I was like, there must not be anything new about it, you know, just another similar kind of feature with a different name. But I was wrong! It seems very powerful feature to me at least!

What I did was nothing special. Googled it and went through tons of articles. Most of them are filled with the official documentation but not the simple explanation and some of them are with nice decent explanation. I couldn't understand most of it, to be frank. I was wondering why the feature is so hard to get hold of! So, I tried to play with it and find out more about it. Before I show some of my findings let's just go through some crappy theory first!

**As per the official documentation, SELECT DISTINCT ON ( expression [, ...] ) keeps only the first row of each set of rows where the given expressions evaluate to equal.**

> In simple terms, if we sue DISTINCT ON then it will give us the first result from the set of results which are grouped together.

*Now the question is, when did we group them? We just simply use DISTINCT ON.* Well, with DISTINCT ON, we just want PostgreSQL to return **a single row for each distinct group** **defined by the ON clause.**

> The DISTINCT ON clause will only return the first row based on the DISTINCT ON(column) and ORDER BY clause provided in the query. For other columns, it will return the corresponding values. Basically, it LIMITs 1 by default when we use DISTINCT ON.

The DISTINCT ON expressions are interpreted using the same rules as for ORDER BY. That means we can decide what row we want in our results- but by only ascending and descending the columns.

Note that the "first row" of each set is unpredictable unless ORDER BY is used to ensure that the desired row appears first. That means the results will be different if we don't use ORDER BY as Postgres is not smart enough to know our minds! The results will not be in order basically. For example,

Above example is from official documentation. Now, we are not adding ORDER BY clause in it and that's why we don't know which of the rows will be selected. If we add, ORDER BY like the following example, we can be sure of a specific row.

```
SELECT DISTINCT ON (location) location, time, report
FROM weather_reports
ORDER BY location, time DESC;
```

The query retrieves the most recent weather report for each location.

Now, let's just take a few more examples.

### Is there any difference between the results of DISTINCT and DISTINCT ON queries?

Yes, there is. That's why they have both! Take a look at the queries and results below.

Simple DISTINCT query:

Output:

![DISTINCT%20ON%20The%20confusing,%20unique%20and%20useful%20featu%20e430de86b18242feac7c1d29bc3f5044/distinct-on-query-output-yogesh-chauhan-1.jpg](DISTINCT%20ON%20The%20confusing,%20unique%20and%20useful%20featu%20e430de86b18242feac7c1d29bc3f5044/distinct-on-query-output-yogesh-chauhan-1.jpg)

DISTINCT ON query:

Output:

![DISTINCT%20ON%20The%20confusing,%20unique%20and%20useful%20featu%20e430de86b18242feac7c1d29bc3f5044/distinct-on-query-output-yogesh-chauhan-2.jpg](DISTINCT%20ON%20The%20confusing,%20unique%20and%20useful%20featu%20e430de86b18242feac7c1d29bc3f5044/distinct-on-query-output-yogesh-chauhan-2.jpg)

![DISTINCT%20ON%20The%20confusing,%20unique%20and%20useful%20featu%20e430de86b18242feac7c1d29bc3f5044/distinct-on-query-output-yogesh-chauhan-3.jpg](DISTINCT%20ON%20The%20confusing,%20unique%20and%20useful%20featu%20e430de86b18242feac7c1d29bc3f5044/distinct-on-query-output-yogesh-chauhan-3.jpg)

What about adding ORDER BY?

```
SELECT DISTINCT ON (country) contact_name, country, company_name FROM customers 
ORDER BY country;
```

Output:

![DISTINCT%20ON%20The%20confusing,%20unique%20and%20useful%20featu%20e430de86b18242feac7c1d29bc3f5044/distinct-on-query-output-yogesh-chauhan-4.jpg](DISTINCT%20ON%20The%20confusing,%20unique%20and%20useful%20featu%20e430de86b18242feac7c1d29bc3f5044/distinct-on-query-output-yogesh-chauhan-4.jpg)

There is no difference between the outputs from the previous and the current query. That's because Postgres is showing results in ASC (Ascending) order by default.

### Let's try DSC (Descending) order.

```
SELECT DISTINCT ON (country) contact_name, country, company_name FROM customers 
ORDER BY country DESC;
```

Output:

![DISTINCT%20ON%20The%20confusing,%20unique%20and%20useful%20featu%20e430de86b18242feac7c1d29bc3f5044/distinct-on-query-output-yogesh-chauhan-5.jpg](DISTINCT%20ON%20The%20confusing,%20unique%20and%20useful%20featu%20e430de86b18242feac7c1d29bc3f5044/distinct-on-query-output-yogesh-chauhan-5.jpg)

As we can see, the results are completely different. So, when we use thie DISTINCT ON, we need to be careful what we want in our results.

Now, by this point, we know that it acts like GROUP BY.

### Then, why do we need GROUP BY in Postgres?

Well, let's understand that by queries.

The query above will raise an error as we are not using COUNT or any other aggregate functions as well as we are not adding all the columns to the GROUP BY clause. So, one of those options we need to choose. Either add aggregate function or add all columns to the GROUP BY clause.

The screenshot of the error:

![DISTINCT%20ON%20The%20confusing,%20unique%20and%20useful%20featu%20e430de86b18242feac7c1d29bc3f5044/distinct-on-query-output-yogesh-chauhan-6.jpg](DISTINCT%20ON%20The%20confusing,%20unique%20and%20useful%20featu%20e430de86b18242feac7c1d29bc3f5044/distinct-on-query-output-yogesh-chauhan-6.jpg)

So, if we add all the columns to the GROUP BY clause then we will basically get the same results as just simple DISTINCT query.

```
SELECT country, contact_name, company_name FROM customers 
GROUP BY country, contact_name, company_name;
```

Output:

![DISTINCT%20ON%20The%20confusing,%20unique%20and%20useful%20featu%20e430de86b18242feac7c1d29bc3f5044/distinct-on-query-output-yogesh-chauhan-7.jpg](DISTINCT%20ON%20The%20confusing,%20unique%20and%20useful%20featu%20e430de86b18242feac7c1d29bc3f5044/distinct-on-query-output-yogesh-chauhan-7.jpg)

We can not add an aggregate function to just one column. Take a look at the query and results below.

![DISTINCT%20ON%20The%20confusing,%20unique%20and%20useful%20featu%20e430de86b18242feac7c1d29bc3f5044/distinct-on-query-output-yogesh-chauhan-8.jpg](DISTINCT%20ON%20The%20confusing,%20unique%20and%20useful%20featu%20e430de86b18242feac7c1d29bc3f5044/distinct-on-query-output-yogesh-chauhan-8.jpg)

So, we need to write down query like this:

SELECT country, COUNT(contact_name), COUNT(company_name) FROM customers GROUP BY country;

Output:

![DISTINCT%20ON%20The%20confusing,%20unique%20and%20useful%20featu%20e430de86b18242feac7c1d29bc3f5044/distinct-on-query-output-yogesh-chauhan-9.jpg](DISTINCT%20ON%20The%20confusing,%20unique%20and%20useful%20featu%20e430de86b18242feac7c1d29bc3f5044/distinct-on-query-output-yogesh-chauhan-9.jpg)

So, as we can see in the screenshot above, we are getting the number of rows using GROUP BY but if we want the first result from all those groups, we need to use DISTINCT ON and that's why I consider it a powerful feature of Postgres.

*Sources:*

- *https://www.postgresql.org/docs/9.5/sql-select.html*