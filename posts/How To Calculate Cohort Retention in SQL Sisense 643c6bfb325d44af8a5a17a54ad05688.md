# How To Calculate Cohort Retention in SQL | Sisense

Created: Feb 21, 2020 12:21 PM
URL: https://www.sisense.com/blog/how-to-calculate-cohort-retention-in-sql/

![pd-blog-yoast-how-to-calculate-cohort-retention-in-sql-min.jpg](How%20To%20Calculate%20Cohort%20Retention%20in%20SQL%20Sisense%20643c6bfb325d44af8a5a17a54ad05688/pd-blog-yoast-how-to-calculate-cohort-retention-in-sql-min.jpg)

*SQL is one of the analyst’s most powerful tools. In **SQL Superstar**, we give you actionable advice to help you get the most out of this versatile language and create beautiful, effective queries.* ‍

Losing users sucks. Losing customers really sucks. If you’re a startup, you know that [Retention is King](https://andrewchen.co/retention-is-king/). You should always be measuring and improving your user retention, so you can keep more users over time. In this post, we’ll show you how to calculate user retention on your own data in SQL.

## **Defining retention**

If Gloria used the product on Monday and used the product again on Tuesday, she is a retained user. If Bill used the product on Monday, but not on Tuesday, he is a lapsed user. Retention for Monday is the number of retained users divided by the number of total users. If Gloria and Bill were the only two users on Monday, then retention for Monday is 50%.

## **Calculating basic user retention**

The key to calculating retention is counting users who were active at time #1, then counting how many were active at time #2. An easy way to do this in SQL is to left join your user activity table to itself like so:

```
select *
from activity
left join activity as future_activity on
  activity.user_id = future_activity.user_id
  and activity.date = future_activity.date - interval '1 day'
```

Now, for every row of user activity, we have — in that same row — their activity 1 day in the future. This gives us an ideal table for calculating retention with some simple counts:

```
select
  activity.date, 
  count(distinct activity.user_id) as active_users, 
  count(distinct future_activity.user_id) as retained_users,
  count(distinct future_activity.user_id) / 
    count(distinct activity.user_id)::float as retention
from activity
left join activity as future_activity on
  activity.user_id = future_activity.user_id
  and activity.date = future_activity.date - interval '1 day'
group by 1
```

We get this chart:

For extra credit, change the 1-day retention to 7-day or 30-day to capture a sense of longer-term user engagement.

## **Calculating retention of new vs. existing users**

Often retention is quite different for users who just signed up compared to loyal long-term users. To calculate new user retention, simply join in your users table and only look at activity rows that occurred on the user’s join date:

```
select
  users.date as date,
  count(distinct activity.user_id) as new_users, 
  count(distinct future_activity.user_id) as retained_users,
  count(distinct future_activity.user_id) / 
    count(distinct activity.user_id)::float as retention
from activity
-- Limits activity to activity from new users
join users on
  activity.user_id = users.id 
  and users.date = activity.date
left join activity as future_activity on
  activity.user_id = future_activity.user_id
  and activity.date = future_activity.date - interval '1 day'
group by 1
```

We see that while overall retention is 46%, new user retention is only 5.8%! Now we see why it’s so useful to split out new users. Improving new user retention should clearly be a priority.

To look at returning user retention, simply change:

```
users.date = activity.date
```

to:

```
users.date != activity.date
```

This effectively excludes activity from users who joined that day. Our query now looks like:

```
select
  activity.date as date,
  count(distinct activity.user_id) as new_users, 
  count(distinct future_activity.user_id) as retained_users,
  count(distinct future_activity.user_id) / 
    count(distinct activity.user_id)::float as retention
from activity
-- Limits activity to activity from existing users
join users on 
  activity.user_id = users.id 
  and users.date != activity.date
left join activity as future_activity on
  activity.user_id = future_activity.user_id
  and activity.date = future_activity.date - interval '1 day'
group by 1
```

As expected, existing user retention is higher than the overall average: 66% vs. 46%.

## **Calculating retention in cohorts**

It can be very helpful to compare the retention of users who joined in week A with those who joined in week B. This lets us see if our product changes are improving our retention rate. Ideally we’d end up with a chart like this:

We’ll start by defining a few handy subqueries to simplify the problem: new_user_activity restricts user activity to new users:

```
with new_user_activity as (
  select activity.* from activity
  join users on
    users.id = activity.user_id
    and users.date = activity.date
)
```

Cohort_active_user_count calculates the total number of active users — the denominator in our retention calculation — in each daily cohort:

```
, cohort_active_user_count as (
  select 
    date, count(distinct user_id) as count 
  from new_user_activity
  group by 1
)
```

On top of that, we’ll make a few smaller changes to the main query:

Calculate the retention period — the number days retained — as future_activity.date – new_user_activity.date and group by it. With this grouping, we lose the simple count of active users in the cohort. Fortunately, we thought of this and made our Cohort_active_user_count subquery, which we can join in and use as the denominator.

Finally, we’ll wrap the query in an outer query that makes nice looking output, excludes bogus rows, and sorts.

Without further ado:

```
select date, 'Day '|| to_char(period, 'DD') as period,
  new_users, retained_users, retention 
from (
  select 
    new_user_activity.date as date,
    (future_activity.date 
      - new_user_activity.date) as period,
    max(cohort_size.count) as new_users, -- all equal in group
    count(distinct future_activity.user_id) as retained_users,
    count(distinct future_activity.user_id) / 
      max(cohort_size.count)::float as retention
  from new_user_activity
  left join activity as future_activity on
    new_user_activity.user_id = future_activity.user_id
    and new_user_activity.date < future_activity.date
    and (new_user_activity.date + interval '10 days')
      >= future_activity.date
  left join cohort_active_user_count as cohort_size on 
    new_user_activity.date = cohort_size.date 
  group by 1, 2) t
where period is not null
order by date, period
```

Notice also the range join, [one of our favorite SQL tricks](https://www.sisense.com/blog/range-joins-give-you-accurate-histories/), to get multiple days of retention in one chart.

This results in the table:

With Sisense for Cloud Data Teams, we can automatically pivot the result then color by percentile:

## **Making retention more specific**

Remember how different new user and existing user retention were? You can see the same variations across lots of user segments. It’s worth breaking out retention by: demographics, user acquisition channel, paying vs. non-paying users, or different kinds of activity — viewing, creating, buying, etc.

*David Ganzhorn found his passion for data analysis while at Google on the Ads Quality team, then worked at Periscope Data for 6 years before becoming part of Sisense. His projects have spanned data science, data engineering, and product engineering, including working on the R and Python cloud editor, predictive lead scoring models for sales, and full-stack software performance optimization. When he’s not helping change the world of analytics, David enjoys crafting educational software for his child.*