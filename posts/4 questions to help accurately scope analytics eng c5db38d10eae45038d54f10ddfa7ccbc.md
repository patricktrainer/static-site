# 4 questions to help accurately scope analytics engineering projects

Created: Apr 22, 2020 12:18 PM
Tags: Consulting, Data engineering, Productivity, SQL
URL: https://blog.getdbt.com/4-questions-to-help-you-more-accurately-scope-analytics-engineering-projects/

![4%20questions%20to%20help%20accurately%20scope%20analytics%20eng%20c5db38d10eae45038d54f10ddfa7ccbc/scope-1.jpg](4%20questions%20to%20help%20accurately%20scope%20analytics%20eng%20c5db38d10eae45038d54f10ddfa7ccbc/scope-1.jpg)

At Fishtown Analytics, we sell and deliver analytics engineering projects in two-week sprints, each of which has a fixed price and fixed deliverables. Delivering on such a tight timeline with defined outcomes is intense! And we’ve gotten quite good at it: we’ve now delivered over 1,000 sprints, with over 95% of them delivered on time.

As a result, we’ve gotten really, really good at scoping analytics projects. We’ve found that if we answer four questions up-front, we can significantly reduce the chances of uncovering issues before it’s too late. In fact, **ferreting out issues early is the single most important factor in delivering analytics work on time**. If you spend a week going down one path only to realize it’s a dead end, that’s a tremendous amount of wasted time. It’s critical to anticipate the cul-de-sac before you find yourself stuck there.

Our approach to proactive issue identification has become intuitive—it’s something that we all *just do*, because we’ve all burned our hands on the stove enough times to know better: “I should’ve known I needed to check whether those IDs would map. [Shit](https://www.youtube.com/watch?v=Fr0A7TofowE).”

It’s such an important topic, though, that I wanted to take the time to make our intuitive, tacit knowledge more explicit and share it with the larger community. Because this skill isn’t just for consultants: anyone who is using [Agile on their data team](https://www.locallyoptimistic.com/post/agile-analytics-p1/), or really anyone who manages deadlines on data projects at all, should care.

Why? **Data teams are successful when they build reserves of trust**—that’s how you earn the “trusted advisor” status from all of your business stakeholders, and how you ultimately impact the trajectory of the business. We earn trust by delivering data that is high-quality, tested, and accurate. We also build trust when we set clear expectations about how a project will go and then deliver on them, time after time after time.

Here are the four questions we ask to proactively identify issues and deliver analytics engineering projects on time at Fishtown Analytics.

## Do I have the data from the primary source?

It’s not unusual to have data that is relevant to your problem but is from the wrong system. One common example: your company might have marketing data stored in Marketo, but it is ingested into your data warehouse through an existing Salesforce integration. Using the Marketo data vis-a-vis Salesforce isn’t *wrong*, but it’s *risky*. The two-hop integration will have more opportunities for failure, and the data will likely not be as granular or complete as the primary source data. Better to get all data directly from its originating source.

There are actually tons of examples of this. Should you trust:

- **Shopify’s charges or Stripe’s?** I would choose Stripe’s for financial / revenue use cases and Shopify’s for ecommerce use cases.
- **Mixpanel’s events or Segment’s?** I would almost always choose Segment, given that most companies push data through Segment to Mixpanel.
- **Hubspot’s attribution or Snowplow’s?** I believe your web analytics tool (Snowplow in this case) needs to be the authoritative source of your web event data, and thus your attribution.

It’s a funny thing to insist on having data directly from the source when you start a project, because in some ways it’s not very pragmatic. Paying for an extra integration typically has a clear price tag, and it’s not at all clear what the value is at the outset. Why isn’t the data you have “good enough”? The answer is that building your analytics on top of the most fundamentally true source of data saves a tremendous amount of wasted time, frustration, workarounds, and spaghetti code in the future.

**If you have true primary source data, you’re virtually omnipotent**: if a question can be answered, you can answer it. If you’re in a meeting with a VP who says “can we slice leads by acquisition source?” the answer will either be “yes” or “the systems we use don’t give us the data to do that”. If you don’t have primary source data, you sometimes end up having to answer “not given our current analytics pipeline”. Not exactly trust-inspiring.

If you don’t have primary source data, do two things:

1. See if you can ingest that data straightforwardly. This could be as easy as setting up a Stitch or Fivetran integration, or it could require a custom integration (if so, let us know, [we might be able to help out](https://www.fishtownanalytics.com/)!).
2. If you can’t get primary source data and need to rely on a secondary source, alert your stakeholders of the potential drawbacks so that everyone goes into the project with the right expectations. Outline the boundaries of the analysis you’ll be able to provide, and the amount of re-work required down the road if you are able to get at the primary source data. There’s nothing inherently wrong with making decisions based on expediency as long as you’ve clearly educated stakeholders on the potential downstream impacts.

## 2. Is source data sufficiently granular?

According to [Kimball](https://www.kimballgroup.com/2007/07/keep-to-the-grain-in-dimensional-modeling/), it’s important to “stick to rich, expressive, atomic-level data that’s closely connected to the original source and collection process.” I couldn’t agree more: granular data gives you *options*, aggregated data is limiting.

One of the most common examples of this in practice is the difference between Google Analytics data exported via the API and Google Analytics 360 data loaded automatically into Bigquery. Via the API, GA will only give you aggregated metrics, whereas GA 360 will export every single session and every single event into Bigquery. The aggregated data is only useful when creating extremely high-level analyses: trendlines of page views or unique visitors. With the granular data, you can answer any question you want—multi-touch attribution, funnel analysis, A/B testing, etc.

Ideally, you want to have access to the absolute most granular data available from the source data system. At this early stage, you don’t yet know all of the followup questions you’re going to be asked to investigate, and you want to be able to follow the trail wherever it leads. Even if your top-level question could be answered by an aggregated export, your followup questions almost definitely won’t.

It’s important to actually learn about the source data systems whose data you’re interacting with.

- **If it’s a SaaS product**, read the API docs. What data will the API give you? Good APIs give you all of the objects you need; *great* APIs will give you change tracking on top of those objects. For example, the Salesforce API will give you a history table containing all opportunities and their state changes since the beginning of your account. It turns out, that opportunity history table is critical for a big chunk of Salesforce pipeline reporting.
- **If it’s an internal product database**, read whatever internal documentation is available or sit down with an experienced engineer to understand what data is stored in the product.

Overall, the closer you can get to events, the better off you’ll be. If you have all state changes for a given system, you can always reconstruct the state at any given point in time—a very powerful position to be in. For example, the only endpoint you actually need from the Stripe API is the events endpoint: from that single endpoint you can derive the outputs from all other endpoints at any point in time. You can do a similar thing for email marketing performance using Mailchimp’s events table.

Fortunately, most Stitch and Fivetran integrations pull maximally granular data by default—both of these products were built for the modern analytics stack and want to give you complete control. It’s important to check for yourself, though. A little while ago I was speccing out a sprint with a client to do sales pipeline reporting on top of the Stitch Close.io integration, and it turns out that integration (which is community-supported) didn’t include the opportunity history endpoint. This dramatically changed the scope of the project as we couldn’t actually produce the analysis required without adding that additional endpoint to the integration. Better that we discovered that at the outset.

## 3. Has this data set been used before?

If your organization *has not* previously used the data from a given ingestion pipeline, you should treat it as guilty until proven innocent. There are a large number of ways in which data that you haven’t used before can be wrong, and many of them are subtle. There are two main categories:

- **Broken ingestion.** There can be errors in the ingestion that cause data in your warehouse to be incorrect. Even when you’re dealing with Stitch and Fivetran integrations, *shit happens*. Every time I’ve seen an integration break it is for the strangest, most esoteric problems, each is one-of-a-kind.
- **Unanticipated ingestion behavior.** Sometimes, loading happens in a way that you wouldn’t have anticipated. For example, Stitch loads many tables that it calls “reporting tables” as an immutable log and then gives specific instructions on how to query from these tables. If you don’t read their instructions and simply start writing queries, you’ll come up with numbers that are head-scratchingly off.

Both of these types of errors can be caught by *auditing the data* from new data sets before building mission-critical analyses on top of them. What exactly does auditing a data set mean? For us, it means producing straightforward metrics on top of the table/tables that can be compared to the outputs from another system (typically the system that the data was extracted from). For instance, we frequently calculate orders and revenue and compare those metrics with the results we get natively in Shopify. Both of these metrics are very straightforward to calculate and if the numbers match you immediately have a high degree of confidence that the data set is in good shape.

Problems with your raw data are typically cross-cutting: they’ll affect all records in a table, or all records in a certain date range. If you audit 2-3 metrics, you can generally feel pretty good about the data quality overall.

If your organization *has* previously used the data from a given ingestion pipeline, it’s incumbent that you invest in learning what’s already been built. If you’re using dbt:

- look up the existing modeling work that’s been done using dbt docs
- read all of the descriptive text for models and columns, and make sure you actually grok the code
- find the authors in the git commit history, and ask them if there are any gotchas you should know about

**🛑Do not just say “screw it” and start your own work from scratch.** The primary source of analytics engineering tech debt and errors result from multiple code bases attempting to transform and analyze fundamentally the same data. Two code paths equates to double the surface area for errors and infinitely more opportunity for confusion. It’s not always easy to follow the work that’s been done before you, but *it’s critically important that you integrate into an existing code base rather than starting from scratch.* I’ve seen teams who are unwilling to write code collaboratively in this way and instead every analyst builds their own silo. **This is a recipe for an incredibly unproductive data team. 🛑**

## 4. Do the necessary keys exist to join all of the data together?

New analysis typically builds on existing concepts by attaching new data to data that has already been modeled. It’s typical to start with your application database or shopping cart, and then spider outwards into other data systems: event tracking, customer success, advertising, email, etc. As you bring each one of these systems into your pipeline and your data model, you’ll need at least one key to join the data in.

It seems like that would be fairly straightforward, but often it just isn’t. Here are some examples:

- You’re registering your trial signups as leads in your Salesforce instance, but the web form on the marketing site that submits to Salesforce doesn’t have the user’s account number at that point in the flow. No key!
- Your event tracking only shows 15,000 identified users over the past week but your application database is confident that there have been 20,000 users logging in over the same time period. The user identification code for your event tracking pipeline is “leaky”—some identify calls are missing! Which ones?
- You want to track customer acquisition cost (CAC) across your entire funnel, starting with ad spend. But when you go to integrate your data from your various ad sources, you realize that the marketing team hasn’t been adding URL parameters to the links they’ve been using! Without these parameters, you have no way of joining data from the rest of your warehouse to the advertising cost data.

This stuff happens *constantly*, and knowing where to look for problems before you hit them is absolutely critical. If you’re missing a key between two systems, it can stop an entire analytics project dead in its tracks, because often a) adding the key involves bringing in stakeholders from other parts of the org, and b) there is no way to retroactively get the data.

Make sure to check your keys before diving in. If they’re missing, go through the effort of working with the stakeholders to create them. This “process instrumentation” is a critical part of what makes a great analytics engineer: you can’t always expect that business processes will naturally spit out the data you need and sometimes you’ll need to roll up your sleeves and make sure it gets gathered.

## Know the answers before you dive in

As a consultant, I have to have a strong process: if I mis-scope a sprint, it probably means that I’m not going to be getting enough sleep over the coming two weeks. Or maybe it means that we lose $$ on the project—the stakes are real. That’s why I (and everyone at Fishtown) is so focused on being good at scoping.

On an internal data team, the stakes are just as high, but the feedback typically isn’t as clear or immediate. Your stakeholders will notice if you consistently miss deadlines or fail to deliver key results, *they just might not say anything to you*. It’s often hard to give direct feedback to colleague —when’s the last time you said something like “Your team’s miss on that deadline led me to miss my committed OKR for the quarter and I’m pissed.”?

Even if it isn’t made explicit, consistent failure by a data team to deliver predictable outcomes damages trust and thereby damages the team’s ability to make an impact on the larger org. Avoid this outcome by identifying issues during the scoping phase of a project and by communicating limitations of your approach with stakeholders.