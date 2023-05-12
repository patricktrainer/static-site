# How to analyze marketing attribution

Created: Apr 24, 2020 10:42 PM
URL: https://blog.getdbt.com/modeling-marketing-attribution/

[How%20to%20analyze%20marketing%20attribution%20c698fcb1c28146d2a52a3d080e0cabfc/photo-1538474705339-e87de81450e8](How%20to%20analyze%20marketing%20attribution%20c698fcb1c28146d2a52a3d080e0cabfc/photo-1538474705339-e87de81450e8)

Marketing attribution is how you understand the marketing channels and tactics that are driving new customers to your business. It’s critical information that every single marketing team in the world wants, and at some point, every analyst will be introduced to the fraught world of marketing attribution. If you would like to understand the full angst that your colleagues in marketing feel about attribution, take a scroll through this thread (I stopped reading after 50 comments):

What's the deal with SaaS marketing attribution? Is anyone actually solving for this or is it a lost cause?I'm talking multiple models as well: first-touch, last-touch, linear, decay, the works...And don't gimme that Google Analytics crap.— Corey Haines 💡 (@coreyhainesco) [February 8, 2020](https://twitter.com/coreyhainesco/status/1225966194869428225?ref_src=twsrc%5Etfw)

What you will find is:

- Products that cost thousands of dollars **every month**, often offering a “black box model” with no transparency whatsoever.
- “Simple”, “out-of-the-box” solutions that are cheap, but only offer insight on a limited slice of data
- Marketers that have completely given up on the problem (“trust your gut”) and are exhausted by vendor promises

Marketers have been told that attribution is a data problem -- “Just get the data and you can have full knowledge of what’s working!” -- when really it’s a data *modeling* problem. The logic of your attribution model, what the data **represents about your business**, is as important as the data volume. And the logic is going to change based on your business. That’s why so many attribution products come up short.

So what do you **actually** need to build an attribution model?

1. Raw data in your warehouse that represents customer interactions with your brand. For ecommerce companies, this is website visits. For B2B customers, it might be conversations with sales teams.
2. SQL

That’s it. Really! By writing SQL on top of raw data you get:

1. **The cheapest attribution model**. This playbook assumes you’re operating within a modern data stack , so you already have the infrastructure that you need in place:  
    - You’re collecting events data with a tool like Snowplow or Segment (though Segment might get a little pricey)
    - You’re extracting data from ad platforms using Stitch or Fivetran
    - You’re loading data into a modern, cloud data warehouse like Snowflake, BigQuery, or Redshift
    - And you’re using dbt so your analysts can model data in SQL
2. **The most flexible attribution model.** You own the business logic and you can extend it however you want, and change it easily when you business changes
3. **The most transparent attribution model.** You’re not relying on vendor logic. If your sales team feels like your attribution is off, show them dbt docs, walk them through the logic of your model, and make modifications with a single line of SQL.

Marketing attribution involves some large data sets, and it is a legitimately fun analytics engineering problem. Let’s talk about how to build the best attribution model your business has ever seen.

## The attribution data model

In reality, it’s impossible to know exactly why someone converted to being a customer. The best thing that we can do as analysts, is provide a pretty good guess. In order to do that, we’re going to use an approach called *positional attribution*. This means, essentially, that we’re going to weight the importance of various touches (customer interactions with a brand) based on their *position* (the order they occur in within the customer’s lifetime).

To do this, we’re going to build a table that represents every “touch” that someone had before becoming a customer, and the channel that led to that touch.

We then estimate the relative weight each touch played in leading to a conversion. This estimation is done by allocating “points” to touches: each conversion is worth exactly one point, and that point is divvied up between the customer’s touches. There are four main ways to divvy up this point:

- **First touch**: Attribute the entire conversion to the first touch
- **Last touch:** Attribute the entire conversion to the last touch
- **Forty-twenty-forty:** Attribute 40% (0.4 points) of the attribution to the first touch, 40% to the last touch, and divide the remaining 20% between all touches in between
- **Linear:** Divide the point equally among all touches

There’s no hard and fast answer to which attribution method you should use — chat with your marketing team about what’s most appropriate for your company.

All in all, here’s what we’re shooting for (this example is for an ecommerce company)

[Untitled](How%20to%20analyze%20marketing%20attribution%20c698fcb1c28146d2a52a3d080e0cabfc/Untitled%20Database%20bc2a77ef086a4742b0c27b59da8e82b1.csv)

Here, we can see that customer `745` had four interactions before converting, they first went to your site after being served a Facebook ad, then they got there via an Adwords ad, and finally they visited your site by typing the URL directly into their browser (twice!) before purchasing.

If you're ready to dive straight into a dbt project to see how this is done, check out our sample attribution project [here](https://www.getdbt.com/attribution-playbook/#!/overview). Otherwise read on for a more in depth explanation.

## How to build an attribution model

### 1. Gather your required data sources

**Sessions:***Required dbt techniques: [packages](https://docs.getdbt.com/docs/package-management)*

We want to use a table that represents every time a customer interacts with our brand. For ecommerce companies, the closest thing we can get to for this is **sessions**. (If you’re instead working for a B2B organization, you should consider using a table of interactions between your sales team and a potential customer from your CRM).

Sessions are discrete periods of activity by a user on a website. The industry standard is to define a session as a series of activities followed by a 30-minute window without any activity.

Here’s an example:

[Untitled](How%20to%20analyze%20marketing%20attribution%20c698fcb1c28146d2a52a3d080e0cabfc/Untitled%20Database%20cf1e3412d1ff4f408b9044fc87ec8981.csv)

Importantly, sessions also have referral information, which helps us understand where a customer came from. These UTM tags are often set by your marketing team, so it’s a good idea to check if they have a master sheet that defines the ones that your company uses. The exact hierarchy for `source`, `medium` and `campaign` often varies from business to business, but here’s what the [Google Analytics docs](https://support.google.com/analytics/answer/1033863) have to say on the topic:

- `utm_source`: The advertiser, site, publication, etc. that is sending traffic to your property, for example: google, newsletter4, billboard.
- `utm_medium`: The advertising or marketing medium, for example: cpc, banner, email newsletter.
- `utm_campaign`: The individual campaign name, slogan, promo code, etc. for a product.

To generate a table of sessions, your website needs to have an event tracking system in place that generates a record for each page view. If you’re only using the free version of Google Analytics, it’s impossible to get that level of granularity in your data. Rather than spend upwards of $100k a year on Google Analytics 360 to get access to the source data, we recommend that you implement the open-source alternative, [Snowplow](https://snowplowanalytics.com/), instead. Segment or Heap are also suitable alternatives if your team is already using them.

Once you have pageviews in your warehouse, you’ll need to do two things

1. **Sessionization:** Aggregate these pageviews into sessions (or “sessionization”) writing logic to identify gaps of 30 minutes or more.
2. **User stitching:** If a user first visits your site without any identifying information (typically a `customer_id` or `email`), and then converts at a later date, their previous (anonymous) sessions should be updated to include their information. Your web tracking system should have a way to link these sessions together.

This modeling is pretty complex, especially for companies with thousands of pageviews a day (thank goodness for [incremental models](https://docs.getdbt.com/docs/configuring-incremental-models) 🙌). Fortunately, some very smart coworkers have written packages to do the heavy lifting for you, whether your page views are tracked with [Snowplow](https://github.com/fishtown-analytics/snowplow), [Segment](https://github.com/fishtown-analytics/segment) or [Heap](https://github.com/fishtown-analytics/heap). Leverage their work by installing the right package to transform the data for you.

**Conversions:**

You’ll also need to know when a customer converted. For a typical ecommerce company, this is the time of a customer’s first order.

You may need to do some transformation to get your data in this shape — use dbt to do this.

### 2. Find all sessions before conversion

We want to limit our analysis to just the sessions that happened before conversion. Join your two data sources together to do this:

```
select
    *
from sessions

left join conversion using (customer_id)

where sessions.started_at <= customer_conversions.converted_at
	and sessions.started_at >= dateadd(days, -30, customer_conversions.converted_at)

```

We often limit the sessions that count towards attribution to just the sessions within the 30 days that preceded conversion (often referred to as an “attribution window”). This is useful when you have a clear idea of your conversion path and it's within a certain time range; if you allow touches to count from forever ago, it can lead to some weird and not-that-useful data.

### 3. Calculate the total sessions and the session index

*Required SQL technique: Window functions*

Once we limit ourselves to the sessions before conversion, we need to know:

- How many sessions did this customer have before conversion? (`total_sessions`)
- What number sessions (of those sessions) is this? (`session_index`)

These fields form the foundation for us to calculate the number of attribution points to assign to each session.

```
select
    *,

    count(*) over (
        partition by customer_id
    ) as total_sessions,

    row_number() over (
        partition by customer_id
        order by sessions.started_at
    ) as session_number

from sessions

left join customer_conversions using (customer_id)

where sessions.started_at <= customer_conversions.converted_at
    and sessions.started_at >= dateadd(days, -30, customer_conversions.converted_at)

```

### 3. Allocate points

Now that we have our `session_index` and `total_session` fields, we’re a few `case` statements away from our attribution points:

```
select
    *,
    case
        when total_sessions = 1 then 1.0
        when total_sessions = 2 then 0.5
        when session_number = 1 then 0.4
        when session_number = total_sessions then 0.4
        else 0.2 / (total_sessions - 2)
    end as forty_twenty_forty_points,

    case
        when session_number = 1 then 1.0
        else 0.0
    end as first_touch_points,

    case
        when session_number = total_sessions then 1.0
        else 0.0
    end as last_touch_points,

    1.0 / total_sessions as linear_points

from sessions_before_conversion

```

**And that’s it!** You’ve built your attribution model! Using these points you can tell which channel and campaign led to the most conversions over time. We leave it to the BI layer to do these sorts of aggregations:

```
-- in your BI tool:
select
    date_trunc(week, converted_at) as date_week,
    utm_campaign,
    sum(first_touch_points) as attribution_points
from attribution
group by 1, 2

```

Depending on your BI tool, you can also explore creating interfaces for stakeholders to toggle between attribution methodologies and the level of aggregation (reporting on day vs week vs month, and grouping by campaign, source, or medium).

Hold up, why are we date-truncing the conversion date here, not the date of the session? When sessions occur, we don’t know if (or when) these will lead to conversions. As a result, if we group by session date, our conversion rates continue to increase every week.

As a marketing team, this can make it hard to make decisions, since the numbers are always changing. So, rather than answering “how many Facebook sessions led to conversions this week?”, we’re choosing to answer “how many conversions this week were a result of Facebook sessions?”.Now that your marketing team knows which channels are leading to the most conversions, they might then ask: “which channel is leading to the **highest value** conversions?”

### 4. [Bonus] Join in revenue value

If you have the dollar value of a conversion available, you should join it to your model!

Simply multiply your points by the conversion value:

```
select
	... ,
    revenue * first_touch_points as first_touch_revenue,
    revenue * last_touch_points as last_touch_revenue,
    revenue * forty_twenty_forty_points as forty_twenty_forty_revenue,
    revenue * linear_points as linear_revenue
from sessions_before_conversion

```

Now that your marketing team knows which channels are leading to the highest value conversions, they might then ask: “which channel is leading to the **best return on my spend**?”

### 5. [Bonus] Join with ad spend data

To do this, you’ll need a clean view of ad spend in your warehouse – one record per campaign, per day, with campaign attributes (channel, source), and amount spent.

To do this, you’ll need to get data from each platform that you spend money on into your warehouse (Adwords, Facebook, Instagram, Bing, etc.). We use Stitch and Fivetran to hit the API of each ad platform and load this data into our warehouse. Since these data sources get loaded in a source-conformed format (i.e. column and tables are named by the API, rather than by us), you’ll need to transform it to get into a consistent structure, then union it together.

[Untitled](How%20to%20analyze%20marketing%20attribution%20c698fcb1c28146d2a52a3d080e0cabfc/Untitled%20Database%202a3a2b1b5d2549579337d8406e27ad53.csv)

(Pro-tip: check out the [dbt package hub](https://hub.getdbt.com/) for some ad-platform specific packages that do the heavy lifting for you!)

Importantly, this data should have the same utm parameters as your session data. That way, we can join across the two data sets to calculate:

- Cost per acquisition: the number of advertising dollars spent to acquire a customer
- Return on ad spend: attributed revenue / ad spend

```
with ad_spend as (

    select * from {{ ref('ad_spend') }}

),

attribution as (

    select * from {{ ref('attribution_touches') }}

),

-- aggregate first as this is easier to debug / often leads to fewer fanouts
ad_spend_aggregated as (

    select
        date_trunc('month', date_day) as date_month,
        utm_source,

        sum(spend) as total_spend

    from ad_spend

    group by 1, 2

),

attribution_aggregated as (

    select
        date_trunc('month', converted_at) as date_month,
        utm_source,

        sum(linear_points) as attribution_points,
        sum(linear_revenue) as attribution_revenue

    from attribution

    group by 1, 2

),

joined as (

    select
        *,
        1.0 * nullif(total_spend, 0) / attribution_points as cost_per_acquisition,
        1.0 * attribution_revenue / nullif(total_spend, 0) as return_on_advertising_spend

    from attribution_aggregated

    full outer join ad_spend_aggregated
    using (date_month, utm_source)

)

select * from joined
order by date_month, utm_source

```

This gives us a view of the data like so:

[Untitled](How%20to%20analyze%20marketing%20attribution%20c698fcb1c28146d2a52a3d080e0cabfc/Untitled%20Database%200befe6274ee2481a823bf580fe2d606b.csv)

There’s a few things worth noting in this query:

- We aggregated in a CTE and then joined the two CTEs together — I get nervous whenever a join and an aggregation are happening in the same query (too much risk of fanout!), splitting up the logic keeps it cleaner, and your query optimizer will thank you.
- It’s rare to see a `full outer join` in the wild! We have one here to ensure that
    - Conversions that don’t have associated ad spend appear in our result set
    - Ad spend that doesn’t result in conversions still appears in our result set
- Often, the utm attributes on your ad spend data won’t perfectly match the utm parameters on your sessions, so you’ll need to do some upstream data cleaning to get this join to work.
- We joined conversion date with ad spend date. As explained above, this prevents numbers changing after the reporting period.This is how most marketing teams approach this problem.

## 6. Ship it!

Now that you have the data, and some working queries, commit it to your dbt project, build some dashboards, and get it into the hands of your stakeholders.

User-test it with your stakeholders to find any issues, and understand whether they are important enough to fix before sharing the dashboard with the wider business. Don’t wait for your work to be perfect before sharing it!

Depending on your BI tool, you can also explore dashboard parameters to:

- Switch between attribution methodologies
- Switch between aggregate level (utm source/medium/campaign)

Once your core stakeholders have tested out your model and find value in it, we recommend that you collaborate with your stakeholders to endorse one attribution method only. All core dashboards should only use this endorsed method — every attribution method is wrong, but it’s important that everyone uses the same version of “wrong”.

## Understanding the limitations of this model

### 1. Positional attribution is not a perfect representation of human decision making

Human beings are complex. There are entire fields dedicated to understanding decision making. As such, it’s likely impossible to accurately answer the question; “what led to a conversion?” with any tool, let alone with some SQL! The benefit of doing it in SQL is that we can be directionally correct, and we retain full control over the model.

With that being said, it’s worth recognizing that this model is best used when looking at the data in aggregate. We recommend that you:

- Roll up to the week level — even grouping by day can become too granular.
- Avoid apportioning dollar spend to a customer: there’s often a desire to be able to “customer 123 cost me $12 to acquire”. Since attribution is an imperfect science, we don’t recommend you do this.

### 2. Ad views aren’t considered in this model

There’s one omission from this analysis: ad views (e.g. when a customer sees one of your ads on Instagram, but doesn’t end up on your website as a result). For most companies, it’s impossible to get records of these ad views into your data warehouse, so you’ll have to rely on the platforms reported metrics for this. Always take these with a grain of salt: it’s in the ad platform’s best interest to report these numbers as highly as they can.

### 3. Web tracking is fickle

Some of your customers will have web tracking turned off, so you’ll never know where this customer came from.

Two of your customers might share a computer, and all of their sessions might be associated with however made a purchase most recently. Or (more likely) one user might have two accounts that they use.

The point is: web tracking is fickle. For some portion of your customer base, the numbers will be slightly off.

## Making it your own

While the big ideas of modeling attribution are consistent across businesses, the nuances of your business will change some details on how you implement this.

If you’re a B2B business, it may be more useful to use interactions with a sales team instead of sessions as your representation of “touches”. These are often logged in a CRM tool — if you’re using Salesforce, check out the “events” and “tasks” tables. Many teams will log impromptu calls as tasks and scheduled meetings as events — work with your sales team to understand how data is recorded at your company.

You’ll also need to consider what defines a “conversion”, especially when conversions are at the account level, but interactions may be at the customer level.

### Bespoke points allocation methodology

Some marketing teams like to implement their own points allocation method. For example, one team that we’ve worked with modified their logic to give paid channels priority:

- If the customer’s journey has no paid, just treat it like standard 40-20-40
- if the customer’s journey does have paid, then as soon as that paid session happens, all subsequent non-paid channels no longer count towards the user’s journey.

The reason behind this? If you found out about a company via adwords or facebook (etc) and then later went to their site via organic search or direct, it’s really that initial ad that is doing all the work there. We’re apportioning credit accordingly.

If you’re an ecommerce company that spends a large portion of your marketing dollars on retargeting existing customers (> $1m a year as a result of thumb), it may make sense to invest in building order-level attribution. Rather than mark the first order as the conversion date, each customer has multiple conversions and each conversion has independent attribution. This is a less-common approach than customer-level attribution, but we’ve worked with several clients who have found this view of their data valuable. If you’re considering doing this, make sure to discuss it with your marketing team first as it’s important that this modeling tracks closely with their beliefs about customer purchase patterns.

Adjust your SQL to find all the sessions before the first order, as well as the sessions between each order — you’ll need to use a window function in an upstream `orders` table to find the date of the previous order. Make sure you use the `order_id` instead of your `customer_id` as the partition clause in your window function

```
select
    *,

    count(*) over (
        partition by order_id
    ) as total_sessions,

    row_number() over (
        partition by order_id
        order by sessions.started_at
    ) as session_number

from sessions

left join orders
    using (customer_id)

where sessions.started_at <= orders.created_at
    and sessions.started_at >= dateadd(days, -30, orders.created_at)
    -- ensure sessions aren't counted twice
    -- use a coalesce to ensure the first order isn't excluded by a NULL join 
    and coalesce(sessions.started_at > orders.previous_created_at, true) 

```

Sessions aren’t the only way that users interact with your brand. It’s common for teams to mix in data from:

- Referral surveys, i.e. “How did you hear about us?” questions
- Promotional code uses
- Out of home (OOH) campaigns, e.g. TV ads and billboards

For sources where you have a record of the interaction (i.e. referral surveys and promo codes), you’ll need to transform this to be in the same shape as sessions, and union it with your data. You’ll also need to codify the business logic of how much weight to give these sessions, for example, should the answer to a survey be weighted more highly than web session?

For sources where you don’t have a record of the interaction (particularly OOH campaigns), you’ll need to make some educated guesses based on the relative uplift of traffic (this is often referred to as spike modeling, but is beyond the scope of this article!).

## Final thoughts:

If you get to the point where you can report on ad spend and conversions side-by-side in a way that’s useful to your marketing team, you are already doing better than most companies.

Then, you’ll encounter a decision point, where you’ll have to answer:

- **Do I invest more time in this model?** Should I use a [markov model](https://medium.com/@mortenhegewald/marketing-channel-attribution-using-markov-chains-101-in-python-78fb181ebf1e), mix in predictive customer lifetime value (CLV), and consider other costs like marketing salaries?
- **Do I invest time in the quality of my source data?** Often the hardest part of this analysis is joining up ad spend and touches, as UTM campaigns are often poorly maintained. Can I work with the marketing team to create *better* UTM schemas?
- **Or, do I move on and tackle another problem?** For many companies, data resources are finite, and investing more time in this model comes at the cost of another project.

Generally, I’d err on the side of options 2 and 3 — too often we see a ton of time and effort go into working on solving attribution, only to have the dashboards never be used. Even if your model is being used, there’s always a risk that you make a model more complex, without making it more useful.

Instead, take a step back, realize that you’ve done some great work, and consider moving on.

 Thanks to Erin Ogilvy, Tristan Handy and Janessa Lantz for their contributions to this playbook.