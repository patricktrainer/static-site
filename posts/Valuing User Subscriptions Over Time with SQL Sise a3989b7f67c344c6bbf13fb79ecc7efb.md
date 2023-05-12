# Valuing User Subscriptions Over Time with SQL | Sisense

Created: Feb 21, 2020 12:21 PM
URL: https://www.sisense.com/blog/calculating-active-subscriptions-over-time/

![yoast-over-time-blog-min.jpg](Valuing%20User%20Subscriptions%20Over%20Time%20with%20SQL%20Sise%20a3989b7f67c344c6bbf13fb79ecc7efb/yoast-over-time-blog-min.jpg)

We recently launched the instant-classic underwater warfare game Scope: Battle for the High Seas, and our investors are excited to see how the game’s subscriptions are growing. We are using a payment processor to handle collections of subscriptions and have access to a few tables. While this makes analyzing the data possible, it is initially not in the best format to do so. Let’s investigate how we can normalize our date ranges to compute the growth of subscriptions since our game launched.

**Starting from the raw data**

Our primary table is a subscription table that has the company id, plan id, and the start and end dates of each plan:

This data structure allows us to easily analyze some date slices of our data. For example, we can look at the number of plans started on a given date:

But it doesn’t allow us to see inside of our start and end ranges, such as how many plans were active on a specific date. In order to do this, we must first get our data into a format friendly for aggregating across our ranges.

## **Getting the relevant dates**

We first want to generate date series for each of our ranges, and we can reference these posts for best practices on doing so: [Generate Series in Redshift and MySQL](https://www.sisense.com/blog/generate-series-in-redshift-and-mysql/) and [Use generate_series to get continuous results](https://www.sisense.com/blog/use-generate-series-to-get-continuous-results/).

In our case, we will opt for Redshift syntax and use a window function to get our date series. Since we only want a limited series of data, we can perform a check using a nested select to make sure that our dates only cover our periods with a plan.

```
with
  dates as (
    select
      (
        getdate()::date - row_number() over(order by true) 
      )::date as plan_date
    from
      subscriptions
  )
  , plan_dates as (
    select
      plan_date
    from
      dates
    where
      plan_date >= (
        select
          min(plan_start)
        from
          subscriptions
      )
  )
```

## **Accounting for null dates**

In our subscriptions table we currently have the dates where they have started and ended. We like to pre-process our data to ensure data consistency when other analysts reuse our work. To ensure that active subscriptions are included in our analysis, we’ll want to give our end dates a value as well. We can accomplish this by using a coalesce statement to evaluate the plan_end value and inserting the current date in the event that it is null:

```
, cleaned_subs as (
  select
    company_id
    , plan_id
    , plan_start
    , coalesce(plan_end, getdate()::date) as plan_end
  from
    subscriptions
)
```

## **Joining on inequalities**

Now that we have our cleaned subscription data in one temp table and our relevant dates in another, we can join them together. We typically join two tables by looking for equal attributes, but we are certainly not limited to the equality operator. For our analysis, we want our result set to have a set of rows for every date that a plan was active.

To do this, we will left join plan_dates to cleaned_subs where the plan_date is greater than or equal to the plan_start and plan_date is less than or equal to the plan_end.

```
, joined_data as (
  select
    *
  from
    plan_dates
    left join cleaned_subs on
      plan_dates.plan_date >= cleaned_subs.plan_start
      and plan_dates.plan_date <= cleaned_subs.plan_end
)
```

Now that we’ve got our data merged together, we are able to see a record in the result set tying every subscription id to every day it was active.

## **Aggregating our data**

Now that our data is joined across date ranges, we can perform the next step in our analysis and aggregate the data! We will use the count function to determine the number of each type of plan that we have by day.

```
, aggregated_data as (
    select
      plan_date
      , plan_id
      , count(*) as active_subs
    from
      joined_data
    group by
      1
      , 2
  )
```

With that, we are able to see the growth of plans over time:

This is great information, but won’t tell the full story to our investors. What we really want to display is how Scope is growing and how its users are signing up and upgrading over time. To get this picture of our data, we can join our aggregated data with our plan data to understand the value within each plan:

```
select
  plan_date
  , plan_id
  , plan
  , (active_subs * amount) as mrr
from
  aggregated_data
  join plans on
    aggregated_data.plan_id = plans.id
```

Now we are able to see that our users are in fact moving from our Starter plan to a Pro Plan over time and that the growth in revenue is promising!

Pushing joins beyond their normal use cases opens the door to analyze data beyond its initial state.