# The four priorities for an analytics team of one–lessons from Lola.com

Created: Feb 21, 2020 12:03 PM
URL: https://blog.getdbt.com/the-four-priorities-of-an-analytics-team-of-one-lessons-from-lola-com/

[The%20four%20priorities%20for%20an%20analytics%20team%20of%20one%E2%80%93l%20cbea2e5b4b1d42018105509c38df68db/photo-1525103504173-8dc1582c7430](The%20four%20priorities%20for%20an%20analytics%20team%20of%20one%E2%80%93l%20cbea2e5b4b1d42018105509c38df68db/photo-1525103504173-8dc1582c7430)

Sagar Velagala was the first analytics hire at [Lola.com](https://www.lola.com/), a fast-growing startup with ~$80M in funding and ~100 employees. If Sagar were an average analyst working in Excel, this role would be a nightmare—there’s just no way one analyst could meet the data needs of the entire organization. And if this story had been playing out five years ago, prior to the advent of modern data tools that gives data analysts so much leverage, things wouldn’t have been much better. As it is, he’s nine months into his role and successfully supporting the entire organization with no current plans to hire more people on the data team.

“The traditional analyst workflow–downloading data from multiple SaaS tools, applying business logic in Excel, the monthly reporting treadmill–it doesn’t scale,” Sagar says. “In organizations using traditional analyst workflows, the number of analysts always grows in proportion to company headcount.” He wasn’t interested in laying the foundation for an analytics function that scaled with more people, **he wanted to build an analytics function that scaled with code.**

Sagar was a [dbt](https://www.getdbt.com/) user before joining Lola and already believed that [analysts should work like software engineers](https://docs.getdbt.com/docs/viewpoint). He says, “This workflow allows me to use technology and code to accelerate my productivity. As an analytics organization of one, I’m able to support the analytics needs of a growing company.” Sounds great in theory, but the reality is that when an analyst joins a company, people expect data, insights, and reports *today*. He prepared for this.

At the start of his tenure at Lola, Sagar laid out his analytics strategy, a 10-page document that described his plan to make Lola a “lean, fact-driven organization.” His plan described an approach that started with enabling business users to self-serve in the near-term–meeting the data needs of the organization today–while he implemented an analytics engineering workflow that would scale to meet future data needs.

It’s common that companies using dbt have analytics teams that are significantly smaller than companies still using traditional workflows, but setting up an analytics engineering workflow takes time. Pulling this feat off as a one-person team is a notable accomplishment. Sagar’s approach is valuable for any data analyst who is ready to get off the analytics treadmill.

## Priority #1: Enable business users to understand what is happening in their department today

Sagar took inspiration from Carl Anderson’s book, [Creating a Data Driven Organization](https://www.amazon.com/Creating-Data-Driven-Organization-Practical-Trenches/dp/1491916915), which outlines the six types of questions that can be answered using analytics:

![The%20four%20priorities%20for%20an%20analytics%20team%20of%20one%E2%80%93l%20cbea2e5b4b1d42018105509c38df68db/Screen-Shot-2019-10-08-at-8.12.51-AM.png](The%20four%20priorities%20for%20an%20analytics%20team%20of%20one%E2%80%93l%20cbea2e5b4b1d42018105509c38df68db/Screen-Shot-2019-10-08-at-8.12.51-AM.png)

Source: Creating A Data Driven Organization: From the Trenches by Carl Anderson

His top priority: “Help business users accurately answer ‘What is happening now?’ and have directionally correct answers on ‘What happened in the past?’” Questions like this can be answered well-enough using the reporting that comes standard with the SaaS products that power your business–Salesforce, Intercom, Shopify–if those reports are set up properly.

At this stage, Sagar simply wanted to ensure that business users had good data that they could use *today* to make better decisions about their work. This doesn’t involve complex analysis, but it’s a foundational set of information that buys an analyst time to implement a more scalable analytics process. However, there are long-term benefits of this work as well–when the time comes to begin consolidating data into a central warehouse, that data is going to be a higher quality. If a report isn’t right in a front-end tool it’s usually because a field isn’t being tracked in quite the right way, better to catch that now than when you’re building your first models inside your data warehouse.

As part of this priority, Sagar was also looking to plug any gaps–where weren’t they collecting data that they should be? He identified event tracking and bug tracking as two gaps for the team. Implementing the right tools and tracking early on meant that, even if there wasn’t a business need for insights from those datasets today, the infrastructure would be in place to answer these questions tomorrow.

## Priority #2: Enable business users to understand what is happening across departments using a single source of truth

In order to get the “insights” level of the six types of analytics questions in the chart above, business users need to be able to look outside of their department. **“Teams are able to execute their core functions using specialized front-end tools,” Sagar says. “But they can’t easily operate cross-functionally without combining different data-sources.”**

- If customers churn after a bad support experience, you won’t know that unless you combine revenue data with data from your help desk.
- If the close rate is improving for sales, the answer might be that your sales training worked or that marketing is running a particularly effective campaign.

Traditionally, analysts have solved the need for these cross-functional insights by living in a world of Excel spreadsheets. Sagar outlines that workflow as looking something like this:

[The%20four%20priorities%20for%20an%20analytics%20team%20of%20one%E2%80%93l%20cbea2e5b4b1d42018105509c38df68db/GJQTI2p4TkqFh8IrUfoyRT4O5-0kgt7asiFFfiuZFwgQGxRGet5U-h97UKVQfZTHjwZ07lmL4fMjjBMHi4lI8l5Z4YFkrugUNlSrJVUP6KuE-NwWXybruoaFdBS81TnsdPR4QLjj](The%20four%20priorities%20for%20an%20analytics%20team%20of%20one%E2%80%93l%20cbea2e5b4b1d42018105509c38df68db/GJQTI2p4TkqFh8IrUfoyRT4O5-0kgt7asiFFfiuZFwgQGxRGet5U-h97UKVQfZTHjwZ07lmL4fMjjBMHi4lI8l5Z4YFkrugUNlSrJVUP6KuE-NwWXybruoaFdBS81TnsdPR4QLjj)

Today, analysts can automate the vast majority of this process. Sagar calls this modern workflow “working in code”. It looks something like this:

[The%20four%20priorities%20for%20an%20analytics%20team%20of%20one%E2%80%93l%20cbea2e5b4b1d42018105509c38df68db/86PtL8djxibPBBQx6bO88SWNR7ryBu1H_6_yMvi21tdsHeLFuDXlC1WUcRtpC9SxENww3GNLW_ZBroW1PBGQtrN3ehMAEmrM7wbdWegK6uX_NyFtXLxuJE0RQiEAk21NPzPvPvVp](The%20four%20priorities%20for%20an%20analytics%20team%20of%20one%E2%80%93l%20cbea2e5b4b1d42018105509c38df68db/86PtL8djxibPBBQx6bO88SWNR7ryBu1H_6_yMvi21tdsHeLFuDXlC1WUcRtpC9SxENww3GNLW_ZBroW1PBGQtrN3ehMAEmrM7wbdWegK6uX_NyFtXLxuJE0RQiEAk21NPzPvPvVp)

He explains, “By writing analysis in code I’m no longer a chokepoint in a recurring business process. **Instead of spending 80% of my time cleaning data, I spend my time building tools that enable business users to do it themselves**, and generating real insights that can help scale the business.” So instead of churning out monthly Excel reports, Sagar’s job is now to:

1. Extract data from front-end tools and load it into Snowflake using an automated data pipeline tool. He chose Stitch.
2. Transform data using dbt to write SQL transformations within the data warehouse.
3. Deliver clean, tested, and ready-to-use data to Looker for analysis.
4. Analyze data and provide insights and recommendations across the organization.

Nine months into his role and Sagar has most of Lola’s core business data migrated to this workflow.

## Priority #3: Empower business users to do their own data exploration

In Sagar’s strategy doc he wrote: “Eventually, the organization will need to explore data and deliver insights at a rate that isn’t possible if all queries must filter through a centralized analytics team. At this point, there are two options:

1. Invest in a large, decentralized analytics team to support growing business needs
2. **Enable business users to explore data sets and generate insights independently**

The emphasis on point #2 is Sagar’s. He went on to write: “Option #2 is significantly more efficient, and achievable by leveraging a modern tech stack. Looker is currently the best business intelligence platform on the market that enables analysts to build data tools for business users, and enable them to support themselves.”

In Sagar’s view, it makes sense for analysts to build some reporting for business users, but long term, “Our goal is to have each vice president be able to do their own data work. You need to be able to own your data.” He points to Airbnb as an inspiration for this approach, “On some teams, 80% of users regularly use data tools, and over 50% regularly query in SQL. They hired the right people and built an [amazing training program](https://medium.com/airbnb-engineering/how-airbnb-is-boosting-data-literacy-with-data-u-intensive-training-a6399dd741a2).”

This is certainly an achievable goal *if* the data end users are given access to is high quality, which Sagar defines as: “accurate, consistent, defined, and complete.” In other words, someone needs to do the preparatory work to get data into a state where even a non-analyst can make sense of it. Sagar uses dbt to deliver high-quality data in two ways:

1. Code (not manual processes) keeps data cleansing transformations and business logic transformations consistent.
2. Data tests catch issues before they impact the end-user.

**“I’ve never felt more confident in my underlying data,”** Sagar says. **“As an analyst, this is a huge relief.”**

## Priority #4: Plan for scale

Even with best-in-class technology and code-based processes, the analytics needs of the organization will eventually grow to a point where “it becomes important to optimize for cost and efficiency.” When Lola reaches that stage, Sagar says that’s when it makes sense to hire data engineers, data scientists, and other business intelligence professionals. “These team members can create custom data tools for internal use, optimize queries and database structure, and create complex statistical models that can provide insight into the future.”

Sagar points out that this is the stage when efficiency becomes important as well. “Some tools that worked at an earlier stage may become unreasonably costly, with better alternatives for specific use cases.” The example he uses here is event tracking. Snowplow Analytics’s open source tool allows companies to track any event across the entire funnel from marketing web traffic and product usage, but the trade-off is a more challenging implementation and more maintenance. It may make sense to choose a more expensive, all-in-one tool to start doing event tracking today, knowing that in the long term you’ll adopt something more customizable and affordable.

## A successful analytics team of one

It took nine months for Sagar to reach this point, and today, he’s moving quickly by doing a few things exceptionally well:

### 📚Develop a good process for managing analytics requests

“I have about 30 analytics requests in my backlog right now,” he says, but he doesn’t seem too stressed. All business leaders can submit analytics requests via an #insights channel in Slack. Requests are then prioritized based on how closely they align with business goals. “Right now, we’re focused on customer acquisition, so analytics requests related to that goal rise to the top.”

### 🏗Maintain a tidy dbt project

“Most of what I’m building today is brand new,” Sagar says. “As you introduce new data sets, KPIs, and analysts, the potential for duplication of metrics and models increases. You’ll start getting more of the ‘this doesn’t match that’ type of questions.” Maintaining a well-organized dbt project helps him be a more effective analytics team of one while also preparing for future scale. A few tips:

- **Staging and mart models:** Sagar follows the convention of using staging models for data cleaning, and marts for storing the business logic of a given business function. “My staging models are where I execute minor transformations like data casting, timestamp conversions, putting everything into lower case, etc,” he says.
- **Exclusion lists:** Sagar uses exclusion lists at the staging layer to clean out things like deleted deal records and test emails. This reduces the volume of data he’s working with in his data marts.
- **Ephemeral models:** To reduce model “clutter” in the database, Sagar leverages ephemeral models and dbt’s capability to specify a schema on a model or folder level. “I place all intermediary models in a PROD_TEMP schema instead of ‘PROD’,” he explains.

### 🔬Test data

Today Sagar uses tests on all of his staging models to catch things like duplicate keys. This one simple test is enough for him to catch most problems–whether that’s an error in the data ingestion process or a change in one of Lola’s systems of record–before they impact the end user. Next on his list is to implement more complex testing that spots more subtle anomalies in the data that the business should address.

### 📊Train decision-makers to self-serve

Clean data and efficient workflows don’t mean much if decision-makers don’t know how to turn the data that comes out into actions. Sagar is currently working on building out new self-service training modules on a regular basis, with topics ranging from “How to Use Looker” to “Interpreting SaaS Unit Economics”.

*Huge thanks to Sagar for sharing your thinking with the dbt community 🙏If you know someone in the community who has done a remarkable job documenting a process, putting their thinking into a clever framework, or has helped you get better at analytics engineering, message me on dbt Slack. We would love to feature them.*