# Using Self Joins To Calculate Your Retention, Churn, And Reactivation Metrics | Sisense

Created: Feb 21, 2020 12:21 PM
URL: https://www.sisense.com/blog/use-self-joins-to-calculate-your-retention-churn-and-reactivation-metrics/

![pd-blog-yoast-retention-churn-and-activation-metrics-min.jpg](Using%20Self%20Joins%20To%20Calculate%20Your%20Retention,%20Chur%201c9f05248de04174a9477503bb6a88c7/pd-blog-yoast-retention-churn-and-activation-metrics-min.jpg)

## **Joining a table to itself**

Most sophisticated user analysis looks at repeat usage: How many users come back? How many don’t? How many come back after an extended absence?

To get at these answers, we have to look at what our current users have done in the past. This is tricky in SQL, which doesn’t have explicit ways to bucket users based on past behavior.

The answer is to join tables to themselves. By using a template like select … from events past_events join events current_events, you can get users’ past activity and current activity in a single row, making it much easier to reason about both at the same time.

In this post, we’ll take you through a few common metrics — retention, churn, and reactivation — and show you how to build them in SQL.

## **Retention**

We’ll start with the most common metric: user retention. Simply put, we want to know how many users were active both last month and this month.

Let’s start by aggregating our events table into a monthly rollup, like so:

```
with monthly_activity as (
  select distinct
    date_trunc('month', created_at) as month,
    user_id
  from events
)
```

Now that we have this table, we’ll join it to itself. The left-hand side of the join will represent this month, and the right-hand side will represent last month. We want to make sure that there’s only one row per current_month per user_id, and that row only gets included in the join if the user was active this month and last.

Here’s the query:

```
with monthly_activity as (
  select distinct
    date_trunc('month', created_at) as month,
    user_id
  from events
)
select
  this_month.month,
  count(distinct user_id)
from monthly_activity this_month
join monthly_activity last_month
  on this_month.user_id = last_month.user_id
  and this_month.month = add_months(last_month.month,1)
group by month
```

Our two join conditions are:

1. this_month.month = add_months(last_month.month,1): This sets up how the join works. We want rows that include activity from this month and activity from last month, so we can reason about both time periods in the same statement.
2. this_month.user_id = last_month.user_id: Ensures one row per user_id, and importantly, excludes rows where the user wasn’t present both months.

Together, these two conditions give us a table containing only retained users every month, which we simply group and count over!

## **Churn**

Now we’ll take retention and turn it on its head: How many users last month did not come back this month?

We’ll use the same self join, except this time, we want to only include rows in last_month that do not have equivalents in this_month. Here’s the query:

```
with monthly_activity as (
  select distinct
    date_trunc('month', created_at) as month,
    user_id
  from events
)
select
  last_month.month + add_months(last_month.month,1),
  count(distinct last_month.user_id)
from monthly_activity last_month
left join monthly_activity this_month
  on this_month.user_id = last_month.user_id
  and this_month.month = add_months(last_month.month,1)
where this_month.user_id is null
group by 1
```

We’ve changed our query in two ways:

1. left join: This includes every row from last month, not just the ones with users who were active this month. This sets up the next step:
2. where this_month.user_id is null: After the join, we filter out rows where the user was active this month.

This leaves us with a table of users who were active last month but not this month, which once again we can group and count over!

## **Reactivated Users**

Reactivated Users are users who previously churned, but have now come back. Perhaps they had a renewed need for the product, or perhaps your compelling email retention campaign swayed them.

For reactivated users, we’ll introduce a new table, containing users’ first active months. Here it is:

```
with first_activity as (
  select user_id, date(min(created_at)) as month
  from events
  group by 1
)
```

We’re going to include all active users each month for whom:

1. This is not their first month (because then they’d be new).
2. They were not active the previous month (because then they’d be retained).

Here’s how we do it:

```
with
monthly_activity as (
  select distinct
    date_trunc('month', created_at) as month,
    user_id
  from events
),
first_activity as (
  select user_id, date(min(created_at)) as month
  from events
  group by 1
)
select
  this_month.month,
  count(distinct user_id)
from monthly_activity this_month
left join monthly_activity last_month
  on this_month.user_id = last_month.user_id
  and this_month.month = add_months(last_month.month,1)
join first_activity
  on this_month.user_id = first_activity.user_id
  and first_activity.month != this_month.month
where last_month.user_id is null
group by 1
```

Similar to our Churn query, we employ a couple things in tandem:

1. left join: We want every activity from the current month, even if they weren’t active last month.
2. where last_month.user_id is null: This is the reverse of the trick we used for our Churn query. We want only users who were active this month and not last month.
3. join first_activity … on first_activity.month != this_month.month: This clause excludes new users who joined this month.

Combined together, we get users who were active this month, were not active last month, and are not new: Reactivated users!

## **Percent Change**

Oftentimes it’s useful to know how much a key metric, such as monthly active users, changed between months. We follow a similar methodology for this metric, employing a self join.

Here’s the query:

```
with monthly_active_users as (
 select
   date_trunc('month', created_at) as month,
   count (distinct user_id) as mau
 from events
 group by 1
)
select
 this_month.month,
 [(this_month.mau - last_month.mau)*1.0/last_month.mau:%] as pct_change
from monthly_active_users this_month
join monthly_active_users last_month
 on this_month.month = add_months(last_month.month,1)
```

The above query uses Sisense for Cloud Data Teams’ :[% formatter](https://dtdocs.sisense.com/article/sql-formatters-dollars-percent#content) to convert the decimal into a percentage. Additionally, notice how we multiply the numerator (this_month.mau – last_month.mau) by 1.0 so the SQL output is a float rather than a rounded integer.