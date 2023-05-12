# Building a Mature Analytics Workflow

Created: Feb 21, 2020 12:07 PM
URL: https://blog.fishtownanalytics.com/building-a-mature-analytics-workflow/

![Building%20a%20Mature%20Analytics%20Workflow%2044eac2a675ff4db9b18d0ba5aa1e067d/barn-images-t5YUoHW6zRo-unsplash--1-.jpg](Building%20a%20Mature%20Analytics%20Workflow%2044eac2a675ff4db9b18d0ba5aa1e067d/barn-images-t5YUoHW6zRo-unsplash--1-.jpg)

Over the past year, I and the folks at RJMetrics have had the opportunity to observe, and participate in, a significant evolution of the analytics ecosystem. The center of gravity in mature analytics organizations has shifted away from proprietary, end-to-end tools towards more composable solutions made up of:

- data integration scripts and/or tools,
- high-performance analytic databases,
- SQL, R, and/or Python, and
- visualization tools.

This change has unlocked a world of possibility, but analytics teams (ours included) have still faced challenges in consistently delivering high-quality, low-latency analytics.

Part of our response to these challenges has been the development of our second product, [RJMetrics Pipeline](https://rjmetrics.com/product/pipeline). But having reliable access to data in an analytic database is only part of the challenge that teams are facing today. This post outlines our understanding of these challenges and the efforts we’re undertaking to solve them.

Analytics teams have a workflow problem today. Too often, analysts operate in isolation, and this creates suboptimal outcomes. Knowledge is siloed. We too often rewrite analyses that a colleague had already written. We fail to grasp the nuances of datasets that we’re less familiar with. We differ in our calculations of a shared metric. As a result, organizations suffer from reduced decision speed and reduced decision quality.

Analytics doesn’t have to be this way. In fact, the playbook for solving these problems already exists — on our software engineering teams.

The same techniques that software engineering teams use to collaborate on the rapid creation of quality applications can apply to analytics. We believe it’s time to build an open set of tools and processes to make that happen.

### Analytics is collaborative

Most of the problems with the current analytics workflow aren’t so bad if you’re working alone. You know about all of the data available to you, you know what it means, and you know how it was created. But you don’t scale. As soon as your analytics needs grow beyond a single analyst, these problems begin to manifest.

We believe a mature analytics team’s techniques and workflow should have the following collaboration features:

### **Version Control**

Analytic code — whether it’s Python, SQL, Java, or anything else — should be version controlled. Analysis changes as data and businesses evolve, and it’s important to know who changed what, when.

Bad data can lead to bad analyses, and bad analyses can lead to bad decisions. Any code that generates data or analysis should be reviewed and tested.

### **Documentation**

Your analysis is a software application, and, like every other software application, people are going to have questions about how to use it. Even though it might seem simple, in reality the “Revenue” line you’re showing could mean dozens of things. Your code should come packaged with a basic description of how it should be interpreted, and your team should be able to add to that documentation as additional questions arise.

Further, your analysis may need to be extended or modified by another member of your team, so document any portions of the code that may benefit from clarification.

### **Modularity**

If you build a series of analyses about your company’s revenue, and your colleague does as well, you should use the same input data. Copy-paste is not a good approach here — if the definition of the underlying set changes, it will need to be updated everywhere it was used. Instead, think of the schema of a data set as its public interface. Create tables, views, or other data sets that expose a consistent schema and can be modified if business logic changes.

### Analytic code is an asset

Data collection, processing, and analysis have all grown exponentially in capability in the past decades. As a result, analytics as a practice provides more value than ever to organizations.

> Today, the success of an organization can be directly linked to its ability to make effective, fast decisions based on data.

If analytics is core to the success of an organization, the code, processes, and tooling required to produce that analysis are core organizational investments.We believe a mature analytics organization’s workflow should have the following characteristics so as to protect and grow that investment:

### **Environments**

Analytics requires multiple environments. Analysts need the freedom to work without impacting users, while users need service level guarantees so that they can trust the data they rely on to do their jobs.

### **Service level guarantees**

Analytics teams should stand behind the accuracy of all analysis that has been promoted to production. Errors should be treated with the same level of urgency as bugs in a production product. Any code being retired from production should go through a deprecation process.

### **Design for maintainability**

Most of the cost involved in software development is in the maintenance phase. Because of this, software engineers write code with an eye towards maintainability.

Analytic code, however, is often fragile. Changes in underlying data break most analytic code in ways that are hard to predict and to fix.

Analytic code should be written with an eye towards maintainability. Future changes to the schema and data should be anticipated and code should be written to minimize the corresponding impact.

### Analytics workflows require automated tools

Frequently, much of an analytic workflow is manual. Piping data from source to destination, from stage to stage, can eat up a majority of an analyst’s time. Software engineers build extensive tooling to support the manual portions of their jobs. In order to implement the analytics workflows we are suggesting, similar tools will be required.

Here’s one example of an automated workflow:

1. models and analysis are downloaded from multiple source control repositories,
2. code is configured for the given environment,
3. code is tested, and
4. code is deployed.

Workflows like this should be built to execute with a single command.

Analyst Collective is an open source project created with a single goal: **build tools to facilitate this analytic workflow**. Today, we’re announcing the release of the first version of our initial set of tools:

- **[dbt](https://github.com/analyst-collective/dbt) (data build tool)** is a deployment tool for data models. Today it supports Amazon Redshift. Future versions of dbt will a) extend it to become a package management system, enabling an open source analytics ecosystem, b) automatically run tests on top of data models, and c) extend it to other analytic databases.
- **[analytics](https://github.com/analyst-collective/analytics)** is an open source repository of data models and analysis for common software-as-a-service applications. This code is written using conventions that enable it to be easily portable between organizations using a particular SaaS application. This repository is a proof of concept for the Analyst Collective workflow.
- **[data generator](https://github.com/analyst-collective/data-generator)** is a tool for building robust test datasets. It allows users to specify both the schema and the business logic of a dataset and then generates realistic data conforming to this specification. Data generated in this fashion will play a key role in testing analytic code.

All Analyst Collective code is licensed under the [Apache License v 2.0](http://www.apache.org/licenses/LICENSE-2.0).

Analyst Collective is sponsored by [RJMetrics Pipeline](https://rjmetrics.com/product/pipeline), a tool that helps data engineers and analysts consolidate data into Amazon Redshift. I and the other core Analyst Collective members are employees of RJMetrics and use Pipeline heavily ourselves, but the Analyst Collective Viewpoint and code is equally relevant regardless of how you get your data into Redshift.

With this release we’re officially opening the doors for feedback and contributions from the community. We’d love to hear what you think as we continue to make investments in Analyst Collective. Step through our [getting started guide](http://dbt.readthedocs.io/en/master/) and [join our Slack community](http://ac-slackin.herokuapp.com/)!