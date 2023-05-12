# How to hire an analytics engineer

Created: Mar 31, 2020 3:41 PM
URL: https://blog.getdbt.com/hiring-analytics-engineer/

![How%20to%20hire%20an%20analytics%20engineer%20836b392d4c0b423698814f9ade35913b/room-4uY9123rRzI-unsplash.jpg](How%20to%20hire%20an%20analytics%20engineer%20836b392d4c0b423698814f9ade35913b/room-4uY9123rRzI-unsplash.jpg)

Modern data warehouses like Snowflake, Redshift, and BigQuery have upended the way that data teams function.

Data storage has become cheap and fast.

Data transformation is now done in-warehouse (ELT vs. ETL).

[Data warehouse management has entered the realm of analysts](https://blog.getdbt.com/five-principles-that-will-keep-your-data-warehouse-organized/), not just database administers or data engineers.

**These trends are impacting the way that data teams are staffed and organized.** Increasingly, we’re seeing a new kind of technical analyst begin to adopt the workflows and mental models of their coding counterparts in software engineering. By adopting practices like version control, data testing, and data documentation these analysts become a force multiplier on the data team–bringing process, rigor, and scalability to once-haphazard analytics code.

Many companies still call these people data analysts, but we’ve started to call them “analytics engineers.” It seems to fit–these hybrids sit at the intersection between data analysts and data engineers. They have more engineering skills than your average analyst and are more curious to solve analytical business questions than your average data engineer.

But whatever you call them, plenty of organizations are hiring analytics engineers, and we wanted to get their advice. We talked to 17 data people from Venmo, HubSpot, Billie, Stitch, HotelEngine, and more about what they’ve learned about hiring for this emerging skill set.

## What is an analytics engineer?

An analytics engineer is a technical analyst that applies software engineering best practices to the production and maintenance of analytics code. The analytics engineering workflow cleans and transforms raw data into consumable information and business logic. In the process, the analytics engineering workflow tests data to ensure it is of high quality, documents all business logic, and ensures data models are running reliably in a production environment.

## Why are companies hiring analytics engineers?

### Increase productivity of the data team

It’s still common for data engineers to own 100% of the ETL process in an organization, although this is often a legacy organizational structure from the time when data warehouses weren’t fast enough to allow for data transformation to be done in-warehouse. If you’re using a modern data warehouse, this approach is no longer best practice. For modern data teams, the ideal setup is for analysts, who have a much better understanding of the business logic that goes into data transformation, to own most or all of the transformation process.

An analytics engineer can be that seamless bridge that connects data analysis to data engineering. This role is often the difference between analysts being empowered to turn their work around in real-time vs. needing to wait in the queue to get data engineering support. **It is not uncommon for that difference to result in a 10x in the velocity of the analytical process.**

![How%20to%20hire%20an%20analytics%20engineer%20836b392d4c0b423698814f9ade35913b/Screen-Shot-2019-08-09-at-8.49.51-AM.png](How%20to%20hire%20an%20analytics%20engineer%20836b392d4c0b423698814f9ade35913b/Screen-Shot-2019-08-09-at-8.49.51-AM.png)

Data quality can erode in a few places during the transformation process as an organization matures. Without a tight process, this code can often become full of copy-paste, tables that are no longer used still stick around and create confusion, errors creep in without anyone realizing it, and performance can degrade. All of these issues are simply a byproduct of entropy—the natural state of the world is to degrade towards disorder—and they’ll slow down your team’s productivity significantly.

When data engineers own data transformation, quality erodes because they often don’t quite have the depth of understanding of the business needs that data analysts have. Things get lost in translation, and data engineers aren’t actually able to identify what constitutes an “error state” in the data.

The analytics engineer improves data quality by bringing a deep understanding of what the business needs into the transformation process, but also by bringing the rigor of software engineering to analytics code.

[How%20to%20hire%20an%20analytics%20engineer%20836b392d4c0b423698814f9ade35913b/tDZzmWXsf9tIkQpGS7C7MZkx3LiLghOCxC-gbYaAL3C4nLLi_X53hhnw-3gykjD3e0Odeg66S4GUw9OF7TzbwVKhoLSuAnUAuOmBNEN8mDzlvNDZxH9kvyirQVIDNHFsSCleImSv](How%20to%20hire%20an%20analytics%20engineer%20836b392d4c0b423698814f9ade35913b/tDZzmWXsf9tIkQpGS7C7MZkx3LiLghOCxC-gbYaAL3C4nLLi_X53hhnw-3gykjD3e0Odeg66S4GUw9OF7TzbwVKhoLSuAnUAuOmBNEN8mDzlvNDZxH9kvyirQVIDNHFsSCleImSv)

### Implement specific technology

In some cases, the need for an analytics engineer comes from the fact that organizations are invested in specific tools and workflows. dbt is a tool that is designed to allow analysts to own the entire analytics engineering workflow. Once companies adopt dbt, they start hiring to match that need.

[How%20to%20hire%20an%20analytics%20engineer%20836b392d4c0b423698814f9ade35913b/HVL7Kjgl0z5Kk4uZ0mIMg_cv0ewaJkyWcxl3sOJ-aHqOJm-nVqLTejC0NPE2HoSQVqRpZ9TOhrHgeoPOHLm4j1vvJC_PeQAHDlmXSKz0hpyW6_DCKRkwxXFRPwkHWn5ieNTeorD6](How%20to%20hire%20an%20analytics%20engineer%20836b392d4c0b423698814f9ade35913b/HVL7Kjgl0z5Kk4uZ0mIMg_cv0ewaJkyWcxl3sOJ-aHqOJm-nVqLTejC0NPE2HoSQVqRpZ9TOhrHgeoPOHLm4j1vvJC_PeQAHDlmXSKz0hpyW6_DCKRkwxXFRPwkHWn5ieNTeorD6)

## How do you interview for analytics engineering potential?

It’s unlikely that you’re going to find someone who has “analytics engineer” on their resume. Jillian Corkin, Principal Data Analyst at [HubSpot](https://www.hubspot.com/) advises that hiring managers “focus on the skills you need + the aptitude and interest for learning them. There's a lot of noise in the field and it's not reliable to look at titles. Also, I suspect there's a lot of untapped talent who may not even be thinking about analytics as a career in systems analyst type roles.”

In other words, if you’re hiring for this role, you’ll likely be hiring for potential vs. experience. The people we spoke with pointed to some common indicators of analytics engineering potential.

### 1. They have a natural affinity for structure

Engineers are structured thinkers, and while data analysts haven’t always been taught that same kind of structure, you can often spot a natural affinity for the engineering mindset.

Thoren Palacio from [Venmo](https://venmo.com/) says to look for "a natural passion for structure and efficiency. Does a tidy warehouse bring you joy?” An analytics engineer is steeped in practical problems so Thoren avoids people who are too far on either the data engineering side–“too much reliance on a large engineering infrastructure (e.g. Facebook, Google, Microsoft)–or too far on the business side–“too much experience in non-reproducible workflows (e.g. tools like excel, powerpoint, etc).”

John Lynch, Data Analyst at [CoverWallet](https://www.coverwallet.com/), looks for a minimum of three years of experience as a data analyst and “prior experience working with software engineers or software engineering workflows.” But, like Thoren, he warns that being *too* engineering focused can be a red flag, “We want our analytics engineers to truly be a bridge between engineers and analysts, not just another data engineer.”

Andrej Blaha, Head of BI at [On](https://www.on-running.com/en-us/) also cautions against someone who “wants to build neural networks, but has no real business exposure.”

Emily O’Connell, Talent Acquisition Partner at [Zylo](https://zylo.com/), says one helpful way to suss out natural affinity for engineering workflows is to ask candidates to, “Explain why their data is impactful, valuable, or special.” She says that different types of analysts are motivated by different things. A more traditional data analyst might feel most impactful when someone uses their finished analysis to make a better decision. Whereas an analyst with affinity toward engineering is likely to feel most impactful when they create scale and leverage by delivering trusted, transformed data that *many* analysts can use to improve their productivity.

**Some more interview questions hiring teams use to evaluate this quality include:**

- What are the advantages to a columnar data store? And what are the disadvantages?
- Walk me through the data stacks you've worked with.
- You receive feedback that a source of data has been reporting incorrect data for a couple of weeks and that it has been sent out to multiple clients and been used for internal analyses in the company. How would you go about identifying the root cause of the problem and how would you communicate your findings to all relevant stakeholders?
- What data integrity/governance challenges have you encountered and how did you deal with them?
- Discuss a time you’ve had someone question your analytic work. How did you explain your process and reasoning?

### 2. They are always learning

If you’re hiring for this role, you’re very likely going to be doing some amount of training. Celina Wong from [Simon Data](https://www.simondata.com/), advises that, **“The novice with potential is a better investment than the expert with arrogance.”** Because when you’re hiring for a fundamentally new role, it’s unlikely you’ll find someone who is an expert *in every aspect of the work.* You’re better off looking for someone who loves learning and has the potential to grow.

This approach to hiring isn't all that different from how organizations approach hiring software engineers. Every engineering team has its preferred languages and tooling, but being an expert in those exact languages and tools is rarely a requirement. Yiorgos Boudouris, Manager of Talent Acquisition at [Jobber](https://getjobber.com/) says, “When we are hiring software engineers, we screen more for the ability to learn new things rather than the fact that they know a particular language or framework. We have the same priorities for analytics engineers.”

What's important is that candidates have an interest in learning your team's preferred way of working. A red flag for Jake Stein from [Stitch](https://www.stitchdata.com/) is “lack of curiosity about different methodologies, tools, and philosophies.” Claus Herther, Principal Consultant and Founder at [Calogica](https://calogica.com/) echoes this sentiment, saying a red flag for his team is, "arrogance" and "lack of intellectual curiosity."

Michelle Ballen-Griffin considers it a big plus when someone “is involved in the data community." To her, this signals an interest in staying up-to-date on the latest advancements in the data space as well as helping others with topics that they have expertise in.

Allen Cunningham, Data Engineer at [BookByte](https://www.bookbyte.com/), looks for "curiosity and problem solving." If an analyst isn’t curious about what their counterparts over in data engineering are up to, it might not be the right work for them.

**Some interview questions hiring teams use to evaluate this quality include:**

- What resources (blogs, books, newsletters, etc.) do you follow to keep up with data?
- If you had built the data team and technology stack at your current organization on day one, what would you have done differently?
- When is the last time you learned something new at work just because you were curious about it? What inspired you to take that on?
- What is the most difficult data analysis problem that you have solved to date and how did you do it?
- Tell me a time when you were caught off guard (eg. fire drill project). What was it and how did you handle it?
- Tell me about a project you screwed up and the consequences for the different stakeholders involved. What do you differently now as a result, and how does that impact each of those stakeholders.

### 3. They care about writing damn good SQL

Analytics engineers aren’t afraid of messy data because they can solve it with good SQL. They write SQL in a way that is highly-performant, easy to troubleshoot, and [DRY](https://docs.getdbt.com/docs/design-patterns). They’ll likely write better SQL than either your data analysts or your data engineers.

James Darrell, Data Scientist at [HotelEngine](https://www.hotelengine.com/), looks for these great SQL skills combined with business knowledge “Very strong SQL knowledge and database knowledge, experience working with ‘dirty’ data, collaborative personality and bias for action, passion for the business and digging into the business needs with respect to data, an understanding that good analytical work starts with a good source of data.”

For the [GitLab](https://about.gitlab.com/) team, great SQL skills includes window functions, CTEs, and in general just more complex SQL. Taylor Murphy avoids candidates whose “primary analyst experience is with ‘all in one’ tools, or those who have only worked on data teams where someone else was cleaning the raw data for them.”

At Fishtown Analytics, we’ve hired quite a few analytics engineers and above average SQL is great, but even more than that we look for *an openness to feedback on how to write better SQL*. Analytics engineering involves patterns that can be new and uncomfortable for data analysts, it’s a great sign when analysts who have years of experience with SQL are open and excited to hear ideas on how it could be even better.

Among the group of people we spoke with, the most popular way to test for technical skills is with a technical test. Tests reveal a lot not just how much SQL a candidate knows, but also open up the opportunity for the hiring team to understand how that candidate thinks about writing analytics code with questions like:

- Can you walk me through your thought process here?
- What lead you to define the problem this way?

GitLab asks candidates to rate their SQL skills from 1-5 and then explain why they gave themselves that rating. Bonus points when candidates mention window functions, CTEs, and macros!

## So, where do you find these people?

Seventeen people shared their expertise with us for this article, and while there are some notable trends even among this small group–the traditional job boards work but communities & Meetups are quite popular too–there are less popular ideas with a whole lot of potential–like participating in internship programs. When you’re hiring for a still emerging role, spending 3-6 months showing a group of interns the ropes can be a great way to spot the one or two who have particular aptitude for analytics engineering.

[How%20to%20hire%20an%20analytics%20engineer%20836b392d4c0b423698814f9ade35913b/aVE3fptuXmZSno6hTjwAMET6Km4lBBkgK6q00fHPpb5VrLW-b73D7Ace78SMM7tmO00CSNfXQ-UTANaTAmDhF6o5LzNN7r8I1LAq-xLIOkLUzqMNgyPmOzvX_AdDnWcEyVhowOCx](How%20to%20hire%20an%20analytics%20engineer%20836b392d4c0b423698814f9ade35913b/aVE3fptuXmZSno6hTjwAMET6Km4lBBkgK6q00fHPpb5VrLW-b73D7Ace78SMM7tmO00CSNfXQ-UTANaTAmDhF6o5LzNN7r8I1LAq-xLIOkLUzqMNgyPmOzvX_AdDnWcEyVhowOCx)

If you currently have an open role, there are 1100+ people in the [dbt Slack](https://slack.getdbt.com/) #jobs channel. Join the community, share your role, or just pop in there and get inspired by job descriptions from companies who are currently hiring. A few current openings include:

One word of caution from John Lynch, “Hire one sooner than you think! Analytics engineers are a great way to get data engineers and data analysts/scientists working together more closely.”

We couldn’t agree more.

*Interested in learning more about the day-to-day of an analytics engineer? Check out this video we made with the folks at Monzo bank:*