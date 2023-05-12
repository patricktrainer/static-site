# Scaling Zapier to Automate Billions of Tasks - The Zapier Engineering Blog | Zapier

Created: Jun 18, 2020 3:54 AM
URL: https://zapier.com/engineering/automating-billions-of-tasks/

![Scaling%20Zapier%20to%20Automate%20Billions%20of%20Tasks%20-%20The%205ed5acc7cf2a43f18d91b758df6554e2/ee035dbb65f3bad0efdedee7cef53a02.png](Scaling%20Zapier%20to%20Automate%20Billions%20of%20Tasks%20-%20The%205ed5acc7cf2a43f18d91b758df6554e2/ee035dbb65f3bad0efdedee7cef53a02.png)

> This post is about a year old now, and most of these numbers are about double/triple (either in number of instances or instance sizing). We're actively investigating and rolling out Kubernetes for container orchestration and working on some performance improvements to reduce grief and cost of the infrastructure (which might mean looking into async languages like Golang over Python where appropriate)! ~Bryan, July 25th, 2017

Zapier is a web service that automates data flow between over 500 web apps, including MailChimp, Salesforce, GitHub, and Trello.

Imagine [building a workflow](https://zapier.com/learn/getting-started-guide/multi-step-zaps/) (or a "Zap" as we call it) that triggers when a user fills out your Typeform form, then automatically creates an event on your Google Calendar, sends a Slack notification and finishes up by adding a row to a Google Sheets spreadsheet. That's Zapier. Building Zaps like this is very easy, even for non-technical users, and is infinitely customizable.

As CTO and co-founder, I built much of the original core system, and today lead the engineering team. I'd like to take you on a journey through our stack, how we built it and how we're still improving it today!

## The Teams Behind the Curtains

It takes a lot to make Zapier tick, so we have four distinct teams in engineering:

- The **frontend team** works on the very powerful workflow editor.
- The **full stack team** is cross-functional but focuses on the workflow engine.
- The **devops team** keeps the engine humming.
- The **platform team** helps with QA, and onboards partners to our developer platform.

All told, this involves about 15 engineers (and growing!).

## The Architecture

Our stack isn't going to win any novelty awards—we're using some pretty standard (but awesome) tools to power Zapier. What's more interesting is the ways we're using them to solve our particular brand of problems.

Let's get the basics out of the way first.

### Frontend

We're smack in the middle of transitioning from Backbone to React. We use Babel for ES6 and Webpack + Gulp to compile the frontend. We rely heavily on CodeMirror for some of the more complex input widgets we need, and use React + Redux to do much of the heavy lifting for the uber-powerful Zap editor.

### Backend

Python powers a large majority of our backend. Django is the framework of choice for the HTTP side of things. Celery is a *massive* part of our distributed workflow engine. Most of the routine API work is done with the epic `requests` library (with a bunch of custom adapters and abstractions).

### Data

MySQL is our primary relational data store—you'll find our users, Zaps and more inside MySQL. Memcached and McRouter make an appearance as the ubiquitous caching layer. Other types of data go into other data stores that make more sense for them. For example, in-flight task counts for billing and throttling find themselves in Redis, and Elasticsearch stores historical activity feeds for Zaps. For data analysis we love us some AWS Redshift.

### Platform

Most of our platform is nestled inside our fairly monolithic core Python codebase, but there are lots of interesting offshoots that offer specialized functionality. The best example might be how we utilize AWS Lambda to run partner/user provided code to customize app behavior and API communication.

### Infrastructure

Since Zapier runs on AWS, we have quite a bit of power at our fingertips. EC2 and VPC are the centerpiece there, though we do use RDS where possible along with copious numbers of autoscaling groups to ensure the pool of servers are in tip-top shape. Jenkins, Terraform, Puppet and Ansible are all daily tools for the devops team. For monitoring, we can't rave enough about Statsd, Graylog, and Sentry (they're *so good*).

## Some Rough Numbers

These numbers represent a rough minimum to help the reader gauge the general size and dimensions of Zapier's architecture:

- over 8m tasks automated daily
- over 60m API calls daily
- over 10m inbound webhooks daily
- ~12 c3.2xlarge boxes running HTTP behind ELB
- ~100 m3.2xlarge background workers running Celery (split amongst polling, hooks, email, misc)
- ~3 m3.medium RabbitMQ nodes in a cluster
- ~4 r3.2xlarge Redis instances - one hot, two failover, one backup/imaging
- ~12 m2.xlarge Memcached instances behind ~6 c3.xlarge McRouter instances
- ~10 m3.xlarge ElasticSearch instances behind ~3 m3.xlarge no-data ElasticSearch instances
- ~6 m3.xlarge ElasticSearch instances behind ~1 c3.2xlarge Graylog server
- ~10 dc1.large Redshift nodes in a cluster
- 1 master db.m2.2xlarge RDS MySQL instance w/ ~2 more replicas for both production reads and analysis
- a handful of supporting RDS MySQL instance (more details below)
- …and tons of microservices and miscellaneous specialty services

## Improving the Architecture

While the broad strokes of the architecture remain the same—we've only performed a few massive migrations—a lot of work has been done to grow the product in two categories:

1. Supporting big new product features
2. Scaling the application for more users

Let's dive into some examples of each, with as many nitty-gritty details as possible without getting bogged down!

### Big Features like Multi-Step Zaps

![Scaling%20Zapier%20to%20Automate%20Billions%20of%20Tasks%20-%20The%205ed5acc7cf2a43f18d91b758df6554e2/5bebb901b550aad87f841a04fc81cca7.png](Scaling%20Zapier%20to%20Automate%20Billions%20of%20Tasks%20-%20The%205ed5acc7cf2a43f18d91b758df6554e2/5bebb901b550aad87f841a04fc81cca7.png)

When we started Zapier (fun fact: it was first called Snapier!) at a [Startup Weekend](http://www.columbiastartupweekend.com/?utm_source=zapier.com&utm_medium=referral&utm_campaign=zapier), we laid out the basic architecture in less than 54 hours (fueled by lots of coffee and more than a few beers). Overall, it was decent. We kept the design really, really simple, which was the right call at the time.

Except where it was *too* simple. Specifically, we made Zaps two-stepped: a trigger paired with an action, full stop.

It didn't take long for us to realize the missed opportunity, but the transition was going to be pretty complex. We had to implement a directed rooted tree with support for an arbitrary numbers of steps (nodes), but maintain 1-to-1 support for existing Zaps (of which there were already hundreds of thousands). And we had to do that while preserving support for hundreds of independent partner APIs.

Starting at the data model, we built a very simple directed rooted tree implementation in MySQL. Just imagine a table where every row has a self-referencing `parent_id` foreign key, plus an extra `root_id` foreign key to simplify queries, and you pretty much got it. We discussed switching to a proper graph database (like neo4j) but decided against it because the sorts of queries we make are simple and over isolated graphs of smaller sizes (roughly ~2-50 nodes).

A key aspect to make this work is inter-step independence. Every step has to consume some data (which folder to read from or which list ID to add to, for example), do some API magic, and return some data (say, the new file created or the new card added to a list), but otherwise be ignorant of its placement in the workflow. Each independent step is as dumb as a rock.

In the middle exists the omniscient workflow engine which coordinates independent Celery tasks by stringing together steps as tasks—one step feeding into the next as defined by the Zap's directed rooted tree. This omniscient engine also houses all the other goodies like error & retry handling, reporting, logging, throttling and more.

Even after we nailed the backend support, we had another huge problem: **how do you build a UI for this thing?**

First, you make sure you have some *amazing* designers and JavaScript engineers on the team. Then you wrestle with nested Backbone views for a while before moving onto React. :-) In all seriousness: React is a godsend for the sorts of complex interfaces we are building.

One of the unique things about React is the performance characteristics are developer friendly, but only as long as you have your data figured out. If you aren't using immutable data structures, you should use some structural sharing library to do all mutations, along with deep `Object.freeze()` in development to catch spots where you attempt mutation directly.

There are tons of challenges in building such a complex UI, much of it around testing and feedback, but a huge amount of time was spent just getting the long-tailed data from different APIs to fit elegantly into the same places. Just about every weird shape of data has to be accounted for.

Finally, we were tasked with getting the new editor in front of users for alpha and beta testing. To do this we shipped both versions of the editor simultaneously and used feature switches to opt users in. We did months and months of testing and tweaking before we were happy with the result—you can check out the [Multi-Step Zap launch page](https://zapier.com/learn/getting-started-guide/multi-step-zaps/) to get an idea of where it ended up.

**Related:** Product designer Stephanie Briones details our behind-the-scenes design work in a guest post for the InVision blog, "[Redesigning an Interactive Editor](http://blog.invisionapp.com/redesigning-interactive-editor/?utm_source=zapier.com&utm_medium=referral&utm_campaign=zapier).

### Scaling the Application

It would all be for nought if the service isn't up and running reliably. As such, much of our attention is focused jointly on application design to support horizontal scalability *and* redundant infrastructure to ensure availability.

Some of the wiser decisions we've made so far is to double down on tech we're comfortable with and spin out isolated functionality when we hit a bottleneck. The key is to reuse the exact same solution and move it to another box where it is free to roam fresh pastures of CPU and RAM.

For example, over the last year or so we noticed session data had eaten up a ton of our primary database's IO and storage. Since session data is effectively a key/value arrangement with softer consistency requirements, we heavily debated options like Cassandra or Riak (or even Redis!), but ultimately decided to stand up a dedicated MySQL instance with a single sessions table.

Our instinct as engineers was to find the tool best suited to the job, but as a practical matter, the job didn't warrant additional operational complexity. We know MySQL, it can do simple key/value storage and our application already supports it. Talk about a no-brainer.

Further, careful design of the application can make horizontal scaling equally simple. Long running background tasks (like our Multi-Step Zaps) aren't bound by strict consistency requirements due to their light write pattern, so it is trivial (and safe!) to use MySQL read-only replicas as the *primary* touch point. Even if we occasionally get horrible replica lag measured in the minutes, 99.9% of Zaps aren't changing—and certainly aren't changing soon—so they continue to hum along.

Another good practice is to assume the worst. Design for failure from the beginning. While usually this is easier said than done, nowadays it is actually surprisingly easy to do. For starters: use auto scaling groups with auto-replacement. A common misconception is that ASGs are only for scaling to accommodate fluctuating load. **Wrong!** The ASG + ELB combo can be your backbone of reliability, one that enables you to randomly kill instances without worry since they get replaced in quick order.

Somehow we keep re-learning that the simpler the system is, the better you'll sleep.

## The Day-To-Day

Locally, our engineers enjoy a fully functioning environment courtesy of Docker. `docker-machine` and `docker-compose` together stand up proper versions of MySQL, Memcached, Redis, Elasticsearch as well as all the web and background workers. We generally recommend running `npm` and even `runserver` locally, as file watching is kind of broken with VirtualBox.

The canonical GitHub "pull request model" drives most of our projects that are engineering focused, where day-to-day work is logged and final code review happens before merging. Hackpad houses the majority of our documentation, including copious onboarding documentation.

A big thing at Zapier is [all hands support](https://zapier.com/learn/customer-support/everyone-on-support/). Every four or five weeks, every engineer spends a full week in support helping debug and fix difficult customer issues. This is hugely important to us as it provides a baseline for understanding customers' pain (plus, you might have to deal with the bug you shipped!).

For CI and deployment, we use Jenkins to run tests on every commit in every PR as well as to provide a "one-click deploy" that anyone at the company can press. It's not uncommon for a new engineer to click the deploy button the first week on the job!

We have a full staging environment in a standalone VPC, as well as a handful of standalone web boxes perfect for testing long lived pull requests. Canary deploys to production are common — complete with full logs of any errors courtesy of Graylog.

## You Can Zapier, Too!

Developers can use Zapier to do some pretty awesome stuff.

In addition to Multi-Step Zaps, we've also launched the ability to write [Python](https://zapier.com/help/code-python/) and [JavaScript](https://zapier.com/help/code/) as Code steps in your workflow. No need to host and run scripts yourself — we take care of all of that. We also provide bindings to call out to the web (`requests` and `fetch`) and even store a bit of state between runs!

Our users are employing [Code steps](https://zapier.com/blog/zapier-code/) to build Slack bots (and games!), to replace one-off scripts and lots more. I personally use Code steps to write bots and tools to track code & bug metrics to a spreadsheet, transform oddly formatted data and replace a *ton* of crontabs.

Or, if you have an API that you want non-developers to be able to consume, we have a pretty epic [Developer Platform](https://zapier.com/platform), too. Simply define your triggers, searches and actions, and any user can mix your API into their workflows and integrate your app with over 500 apps like GitHub, Salesforce, Google Docs, and more.

And, we are often hiring, so keep an eye on our [jobs page](https://zapier.com/about/) if you'd like to help us help people work faster and automate their most tedious tasks!