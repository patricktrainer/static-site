# Why Robinhood uses Airflow - Robinhood Engineering

Created: Jun 12, 2020 10:55 PM
URL: https://robinhood.engineering/why-robinhood-uses-airflow-aed13a9a90c8

![1*CcxrRbffqn45YwGglCyexw.png](Why%20Robinhood%20uses%20Airflow%20-%20Robinhood%20Engineering%206ace662dbdd6450fbb8856fca51c2596/1CcxrRbffqn45YwGglCyexw.png)

Robinhood relies on batch processing jobs at set schedules for a large number of tasks. These jobs range from data analysis and metric aggregations, to brokerage operations such as dividend payouts. We started off with using cron to schedule these jobs but with their growing number and complexity, it became increasingly challenging for us to manage them using cron:

- **Managing dependencies** between jobs was difficult. With cron we would use worst-case expected durations for upstream jobs to schedule downstream jobs. This was getting increasingly harder with scale as the complexity of these jobs and their dependency graphs increased.
- **Failure handling** and alerting had to be managed by the job. We would have to rely on the job, or the on-call engineer to handle retries and upstream failures in the case of dependent jobs.
- **Retrospection** was difficult. We would need to sift through logs or alerts to check how a job may have performed on a certain day in the past.

We decided to move away from cron for our scheduling needs and replace it with something that would solve the above problems. We explored a few open source alternatives like [Pinball](https://github.com/pinterest/pinball), [Azkaban](https://azkaban.github.io/) and [Luigi](https://github.com/spotify/luigi), before finally deciding on [Airflow](http://pythonhosted.org/airflow/index.html).

## Pinball

Pinball, developed at Pinterest, has a lot of features of a distributed, horizontally scalable, workflow management and scheduling system. It solves a lot of the problems mentioned above but the documentation was sparse and the relative size of the community was small.

## Azkaban

Azkaban, developed at LinkedIn, is probably the oldest among the alternatives we considered. It uses properties files to define workflows while most of the newer alternatives use code. This makes it harder to define complex workflows.

## Luigi

Luigi, developed at Spotify, has an active community and probably came the closest to Airflow during our exploration. It uses Python for defining workflows and comes with a simple UI. However, Luigi doesn’t have a scheduler and users still have to rely on cron for scheduling jobs.

Airflow, developed at Airbnb has a growing community and seemed to be the best suited for our purposes. It is a horizontally scalable, distributed workflow management system which allows us to specify complex workflows using Python code.

## Dependency Management

Airflow uses [Operators](https://airflow.incubator.apache.org/concepts.html#operators) as the fundamental unit of abstraction to define tasks, and uses a [DAG](https://airflow.incubator.apache.org/concepts.html#dags) (Directed Acyclic Graph) to define workflows using a set of operators. Operators are extensible which makes customizing workflows easy. Operators are divided into 3 types:

- **Action** operators that perform some action such as executing a Python function or submitting a Spark Job.
- **Transfer** operators that move data between systems such as from Hive to Mysql or from S3 to Hive.
- **Sensors** which trigger downstream tasks in the dependency graph when a certain criteria is met, for example checking for a certain file becoming available on S3 before using it downstream. Sensors are a powerful feature of Airflow allowing us to create complex workflows and easily manage their preconditions.

Below is an example of how the different type of sensors can be used for a typical ETL ([Extract Transform Load](https://en.wikipedia.org/wiki/Extract,_transform,_load)) workflow. The example uses Sensor operators to wait until data is available and uses a Transfer operator to move the data to the required location. An Action operator is then used for the Transform stage followed by using the Transfer operator to load the results. Finally, we use Sensor operators to verify that the result was stored appropriately.

## Failure Handling and Monitoring

Airflow allows us to configure retry policies into individual tasks and also allows us to set up alerting in the case of failures, retries, as well as tasks running [longer than expected](https://airflow.incubator.apache.org/concepts.html#slas). Airflow comes with an intuitive UI with some powerful tools for monitoring and managing jobs. It provides historical views of the jobs and tools to control the state of jobs — such as kill a running job or manually re-running a job. One of the unique features of Airflow is the ability to create charts using job data. This allows us to build custom visualizations to monitor the jobs closely and also acts as a great debugging tool while triaging issues with jobs and scheduling.

## Extensible

Airflow Operators are defined using Python classes. This makes it very easy to define custom, reusable workflows by extending existing operators. We have built a large suite of custom operators in-house, a few notable examples of which are the OpsGenieOperator, DjangoCommandOperator and KafkaLagSensor.

## Smarter Cron

Airflow DAGs are defined using Python code. This allows us to define more complex schedules beyond what cron offers. For example, some of our DAGs need to run only on market open days. With simple cron, we would schedule these to run on all weekdays and handle the market holiday case in the application.

We also use Airflow sensors to run jobs right after market close, while handling market half-days. The following example uses custom operators built for running workflows on complex schedules that dynamically update according to the market hours for a given day.

## Backfills

We use Airflow for metrics aggregations and batch processing of data. With evolving needs, we sometimes need to go back and change how we aggregate certain metrics or add new metrics. This involves running backfills across arbitrary spans of time in the past. Airflow provides a CLI which allows us to run backfills across arbitrary spans of time with a single command, and also allows us to trigger backfills from the UI. We use Celery (built by our very own [Ask Solem](https://medium.com/u/ecdd5b4bb13?source=post_page-----aed13a9a90c8----------------------)) to distribute these tasks across worker boxes. The distribution capabilities of Celery make backfills quick and easy by allowing us to spin up more worker boxes while running backfills.

## Common Pitfalls and Weaknesses

We are currently on Airflow 1.7.1.3 which works well in production but comes with its own set of [weaknesses and pitfalls](https://cwiki.apache.org/confluence/display/AIRFLOW/Common+Pitfalls).

- **Time zone issue** — Airflow relies on the system time zone (instead of UTC) for scheduling. This requires the entire airflow setup to be run in the same time zone.
- The **Scheduler** works separately for scheduled jobs and backfill jobs. This can result in weird outcomes such as backfills not respecting a DAG’s max_active_runs configuration.
- Airflow was built primarily for data batch processing due to which the Airflow designers made a decision to always **schedule jobs for the previous interval**. Hence, a job scheduled to run daily at midnight will pass in the execution date “2016–12–31 00:00:00” to the job’s context when run on “2017–01–01 00:00:00”. This can get confusing especially in the case of jobs running at irregular intervals.
- **Unexpected backfills** — Airflow by default tries to backfill missed runs when resuming a paused DAG or adding a new DAG with a start_date in the past. While this behavior is expected, there is no way to get around this, and can result in issues if a job shouldn’t run out of schedule. Airflow 1.8 introduces the [LatestOnlyOperator](https://github.com/apache/incubator-airflow/blob/master/airflow/operators/latest_only_operator.py) to get around this issue.