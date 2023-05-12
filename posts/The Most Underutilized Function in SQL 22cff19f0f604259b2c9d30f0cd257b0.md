# The Most Underutilized Function in SQL

Created: Jan 13, 2020 7:53 PM
Tags: Data, SQL
URL: https://blog.getdbt.com/the-most-underutilized-function-in-sql/

![The%20Most%20Underutilized%20Function%20in%20SQL%2022cff19f0f604259b2c9d30f0cd257b0/jeshoots-com-VdOO4_HFTWM-unsplash.jpg](The%20Most%20Underutilized%20Function%20in%20SQL%2022cff19f0f604259b2c9d30f0cd257b0/jeshoots-com-VdOO4_HFTWM-unsplash.jpg)

Over the past nine months I’ve worked with over a dozen venture-funded startups to build out their internal analytics. In doing so, there’s a single SQL function that I have come to use surprisingly often. At first it wasn’t at all clear to me why I would want to use this function, but as time goes on I have found ever more uses for it.

What is it? **md5()**. If you’re not familiar, here’s an example snippet from the Redshift docs:

```
select md5('Amazon Redshift');

md5
----------------------------------
f7415e33f972c03abd4f3fed36748f7a
(1 row)
```

Give md5() a varchar and it returns its [MD5 hash](https://en.wikipedia.org/wiki/MD5). Simple…but seemingly pointless. *Why exactly would I want to use that?!*

Great question. In this post I’m going to show you two uses for md5() that make it one of the most powerful tools in my SQL kit.

## #1: Building Yourself a Unique ID

I’m going to make a really strong statement here, but it’s one that I really believe in: **every single [data model](http://dbt.readthedocs.io/en/docs-0.6.0/guide/building-models/) in your warehouse should have a rock solid unique ID**.

It’s extremely common for this not to be the case. One reason is that your source data doesn’t have a unique key—if you’re syncing advertising performance data from Facebook Ads via [Stitch](http://stitchdata.com/) or [Fivetran](http://fivetran.com/), the source data in your ad_insights table doesn’t have a unique key you can rely on. Instead, you have a combination of fields that is reliably unique (in this case date and ad_id). Using that knowledge, you can build yourself a unique id using md5():

```
select 
    md5(date_start::varchar || ad_id::varchar) as insight_id
from 
    stitch_fb_ads.facebook_ads_insights
limit 5;

insight_id
----------------------------------
6d475ea96f23b097b51ed500116d8c5e     822c9429eabb28ccbcd7286836d7cd60     8b7fcd2aff879772ccac4f0f8bcb6a45     8a2cfd7eb1a723c49db47232e73ca29c     10338719dfadb3d4c9d44c608063998a
(5 rows)
```

The resulting hash is a meaningless string of alphanumeric text that functions as a unique identifier for your record. Of course, you could just as easily just create a single concatenated varchar field that performed the same function, but *it’s actually important to obfuscate the underlying logic behind the hash*: you will innately treat the field differently if it looks like an id versus if it looks like a jumble of human-readable text.

There are a couple of reasons why creating a unique id is an important practice:

1. One of the most common causes of error is duplicate values in a key that an analyst was expecting to be unique. Joins on that field will “fan out” a result set in unexpected ways and can cause significant error that is difficult to troubleshoot. To avoid this, only join on fields where you’ve validated the cardinality and constructed a unique key where necessary.
2. Some BI tools require you to have a unique key in order to provide certain functionality. For instance, Looker [symmetric aggregates](https://discourse.looker.com/t/symmetric-aggregates/261) require a unique key in order to function.

We create unique keys for every table and then test uniqueness on this key using [dbt schema tests](http://dbt.readthedocs.io/en/master/guide/testing/). We run these tests multiple times per day on [Sinter](http://sinterdata.com/) and get notifications for any failures. This allows us to be completely confident of the analytics we implement on top of these data models.

## #2: Simplifying Complex Joins

This case is similar to #1 in its execution but it solves a very different puzzle. Imagine the following case. You have the same Facebook Ads dataset as referenced earlier but this time you have a new challenge: join that data to data in your web analytics sessions table so that you can calculate Facebook [ROAS](http://www.verticalrail.com/kb/calculate-roas/).

In this case, your available join keys are the date and your [UTM parameters](https://en.wikipedia.org/wiki/UTM_parameters) (utm_medium, source, campaign, etc). Seems easy, right? Just do a join on all 6 fields and call it a day.

Unfortunately that doesn’t work, for a really simple reason: it’s extremely common for some subset of those fields to be null, and a null doesn’t join to another null. So, that 6-field join is a dead end. You can hack together something incredibly complicated using a bunch of conditional logic, but that code is hideous and performs terribly (I’ve tried it).

Instead, use md5(). In both datasets, you can take the 6 fields we mentioned and concatenate them together into a single string, and then call md5() on the entire string. Here’s a code snippet from a client project where we did exactly this:

You can see that this code is actually building the id on top of even more fields: in this example we’re actually unioning together advertising spend data from 7 different ad channels, and the data from Bing and Adwords is identified by ad_group_id and keyword_id instead of by UTM parameters. The approach extends cleanly.

In the sessions table, you then create the exact same hashed id field. **The resulting join is simple, readable, and easy to use for downstream analysis**:

## Resources

Interested in implementing something like this yourself? Here are a few resources:

- [dbt](https://github.com/fishtown-analytics/dbt)(the open source tool we build and use to do all of our data modeling)

Thanks for reading! I’m definitely curious to hear if anyone has any additional clever uses for md5().