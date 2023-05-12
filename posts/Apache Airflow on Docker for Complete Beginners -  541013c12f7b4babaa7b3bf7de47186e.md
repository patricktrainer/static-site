# Apache Airflow on Docker for Complete Beginners - Justin Gage - Medium

Created: Jan 30, 2020 10:29 AM
URL: https://medium.com/@itunpredictable/apache-airflow-on-docker-for-complete-beginners-cf76cf7b2c9a

Airflow — it’s not just a word Data Scientists use when they fart. It’s a powerful open source tool originally created by Airbnb to design, schedule, and monitor ETL jobs. But what exactly does that mean, and why is the community so excited about it?

## **Background: OLTP vs. OLAP, Analytics Needs, and Warehouses**

Every company starts out with some group of tables and databases that are operation critical. These might be an orders table, a users table, and an items table if you’re an e-commerce company: your production application uses those tables as a backend for your day-to-day operations. This is what we call [OLTP, or Online Transaction Processing](https://www.datawarehouse4u.info/OLTP-vs-OLAP.html). A new user signs up and a row gets added to the users table — mostly insert, update, or delete operations.

As companies mature (this point is getting earlier and earlier these days), they’ll want to start running analytics. How many users do we have? How have our order counts been growing over time? What are our most popular items? These are more complex questions and will tend to require aggregation (sum, average, maximum) as well as a few joins to other tables. We call this OLAP, or Online Analytical Processing.

The most important differences between OLTP and OLAP operations is what their priorities are:

- OLTP’s priority is maintaining data integrity and processing a large number of transactions in a short time span
- OLAP’s priority is query speed, and transactions tend to be batched and at regular intervals (ETL Jobs, which we’ll look at later)

Accordingly, OLTP related queries tend to be simpler, require little aggregation and few joins, while OLAP queries tend be larger, more complex, and require more aggregations and joins.

In your e-commerce app, you might want to insert a new row into the orders table when a user makes a new order. These queries are pretty simple: they’ll probably boil down to something like `INSERT INTO users VALUES x,y,z`.

Answering those analytics-type OLAP questions is a different story though: they tend to involve much more data (aggregating order value over an entire table, for example) and require more joins to other database tables. If we wanted to see the total order value for users who live in New York, we’d need to use both an aggregation (sum of order value from the orders table) and a join (filter for New York addresses from the users table).

Early on in the company lifecycle, OLAP type queries and OLTP type queries will be run on your normal production database — because that’s all you have. But over time, OLAP usually starts to become too burdensome to run on your production tables:

- OLAP queries are more computationally expensive (aggregations, joins)
- OLAP often requires intermediate steps like data cleaning and featurization
- Analytics usually runs at regular time intervals, while OLTP is usually event based (e.g. a user does something, so we hit the database)

For these reasons and more, Bill Inmon, Barry Devlin, and Paul Murphy [developed the concept of a Data Warehouse in the 1980’s](https://en.m.wikipedia.org/wiki/Data_warehouse#History). A warehouse is basically just another database, but it’s not used for production (OLTP) — it’s just for analytics (decision support, in their language). It’s designed and populated with all of the above analytics concerns instead of the OLTP requirements for running your app.

## **ETL Jobs and Cron**

Where things get interesting is how you actually *get data into your warehouse*. A typical modern warehouse setup will have many different types of data, like for example:

These all come from different places, and require unique *jobs* to get the data from the source (extract), do whatever you need to get it ready for analytics (transform), and deposit it in the warehouse (load). This process is called ETL (Extract, Transform, Load), and each individual job we need is called an ETL job. So how exactly do we build those?

The classic approach (other than expensive vendors) has usually been **Cron Jobs**. Cron is a utility that runs in your terminal and lets you run programs at specific intervals (say, 2AM every other day). The code required for the ETL job is packaged into a file and scheduled on Cron. The problem, though, is that *Cron wasn’t built for this type of work, and it shows*. Some of the major issues that data teams face scheduling ETL jobs with Cron:

- ETL jobs fail *all the time* for *a million reasons*, and Cron makes it *very* difficult to debug for a number of reasons
- ETL tends to have a lot of dependencies (on past jobs, for example) and Cron isn’t built to account for that
- Data is getting larger, and modern distributed data stacks (HDFS, Hive, Presto) don’t always work well with Cron

Unsurprisingly, [data teams have been trying to find more sophisticated ways](https://medium.com/videoamp/what-we-learned-migrating-off-cron-to-airflow-b391841a0da4) to schedule and run ETL jobs. Airflow is one of the things we’ve come up with, and it’s pretty great.

## **Introduction to Airflow and Its Core Concepts**

Now we can go back to our original definition of Airflow, and it should make more sense. Airflow lets you:

- Design complex, sophisticated ETL jobs with multiple layers of dependencies
- Schedule jobs to run at any time and wait for their dependencies to finish, with the option to run distributed workloads (using [Celery](http://www.celeryproject.org/))
- Monitor all of your jobs, know exactly where and when they failed, and get detailed logs on what the errors were

It’s important to note that **Airflow is not an ETL tool**, even though that happens to be what it’s used most for. It’s a general purpose workflow scheduler, and that will become clearer as we delve into [different Airflow concepts](https://airflow.apache.org/concepts.html).

***Operators***

Airflow Operators are different types of things that you can do in workflows. If you want to run some Python, you’d use the [Python Operator](https://github.com/apache/airflow/blob/master/airflow/operators/python_operator.py), and if you want to interact with MySQL you’d use the [MySQL Operator](https://github.com/apache/airflow/blob/master/airflow/operators/mysql_operator.py). You can also define your own Operators by extending [Airflow’s Base Operator class](https://github.com/apache/airflow/blob/master/airflow/models/__init__.py) (or any of the others).

***Tasks***

Once you actually create an instance of an Operator, it’s called a Task in Airflow. Tasks are what make up workflows in Airflow, but here they’re called DAGs.

***DAGs***

DAG stands for a Directed Acyclic Graph — it may sound scary, but a DAG is basically just a workflow where tasks lead to other tasks. Tasks can be upstream or downstream of other tasks, which sets a sort of order for how they need to get executed.

The “Directed” part means that order matters, like in the above example: we need to create a staging table before we can insert into it, and we need to create a target table before we can insert into it. DAGs are “Acyclic” — that means that they are not cyclical, and have a clear start and end point.

DAGs are the main way you interact with Airflow: you build them from a bunch of different tasks (we’ll get there), and Airflow executes them in order. It’s relatively simple.

***XComs***

Airflow doesn’t really want you to communicate between Tasks, but if you need to you can use Airflow’s XComs, an abbreviation for cross communication. An XCom is sort of like a centralized Key / Value repository: you can push to it from a Task, and and pull from it from a Task. Airflow automatically populates values like which DAG and which Task an XCom belongs to, which makes it easier to use than just storing data in a table.

***Variables***

Airflow Variables are like XComs, but they’re global and not designed for communicating between tasks. Variables make the most sense for settings and configuration, but you can even upload JSON files as variables.

***Recap***

Airflow Operators let you create Tasks, which you organize into DAGs. You can communicate between Tasks with XComs, and set global state with Variables. That’s most of what you need to know. Here’s a simple version of what a DAG might look like:

## **Practical Needs for Running Airflow**

Assuming you already know what your DAGs will look like and what you want them to accomplish, there are a few things you’ll need to understand and get running first.

***Connections***

If you’re using Airflow for ETL (as you probably are), you’ll need to connect your Airflow deployment to whatever databases you intend to work with. Airflow Connections are, well, connections to your databases.

Creating Connections in Airflow is relatively simple, and just involve your typical username, password, host, and port setup. You can use the Airflow UI to add Connections, or create them (more) automatically through environment variables. If you export AIRFLOW_CONN_MY_DB and pass a database URI, that will create a connection called MyDB.

***Hooks***

Airflow Hooks are — ready for this — connections to your Connections. They’re pretty much identical to the `conn` object you might be familiar with if you use Python with SQL, but Airflow makes it simpler by allowing you to just pass it a Connection ID. If you want a Task to insert data to a Postgres Database, for example, you’d create a [PostgresHook](https://github.com/apache/airflow/blob/master/airflow/hooks/postgres_hook.py) from your Postgres Connection, and use the built in methods like `insert_rows`.

***The Airflow Database***

Airflow uses its own internal database to store credentials and your Airflow history (which DAGs you ran, when you ran them, etc.). It ships with SQLite, but you can use whatever you want. You usually get this initialized by running `airflow initdb`.

***Webserver***

One of Airflow’s awesome-est features is the Webserver, which is the front end GUI that it provides to end users. Running `airflow webserver` will get it started (it usually runs on your localhost’s port 8080), and it’s got a ton of cool stuff. Some really clutch features that you might find yourself using:

- Seeing the structure of your DAG in a graph format
- Checking on all of your DAG runs and seeing when they failed
- Adding and editing Connections
- Looking at how long your tasks typically take in one of your DAGs

The Webserver definitely gives Cron a run for its money, and is probably the most compelling feature Airflow has to offer over Cron for beginners.

***Scheduler***

The Airflow Scheduler is what takes care of actually running all of the DAGs that you’ve created: making sure things run in order, quickly, and how you want them to. The interesting part of the Scheduler though — which you’d normally run with `airflow scheduler` — is how Airflow actually executes your tasks. They’re called Executors, and they’re (surprise!) configurable.

The default Executor for Airflow is the Sequential Executor, which (gasp!) just executes your Tasks locally in order. But [if you want to scale out Airflow](http://stlong0521.github.io/20161023%20-%20Airflow.html) to something more production ready, especially using multiple workers, Airflow has other options. The Celery Executor uses [Python’s Celery package](http://www.celeryproject.org/) to queue tasks as messages, and the [Dask Executor](https://airflow.apache.org/howto/executor/use-dask.html) lets you run Airflow Tasks on a [Dask Cluster](https://docs.dask.org/en/latest/). There’s also a [Mesos Executor](https://airflow.apache.org/howto/executor/use-mesos.html).

## **The Best Way to Actually Get Airflow Started**

You can install Airflow pretty simply through `pip`, but there’s *a lot* of configuration to do upfront. The standard way companies get Airflow going is through Docker, and in particular [this image](https://hub.docker.com/r/puckel/docker-airflow) from some user named [puckel](https://hub.docker.com/u/puckel). If you’re not familiar with Docker, check out [FreeCodeCamp’s conceptual introduction](https://medium.freecodecamp.org/a-beginner-friendly-introduction-to-containers-vms-and-docker-79a9e3e119b) and [DigitalOcean’s tutorial](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-16-04) on how to get it going.

Puckel’s [docker-airflow repo](https://github.com/puckel/docker-airflow) has everything you need to get Airflow up and running, and some basic templates for expanding it out to multiple containers with [Docker Compose](https://docs.docker.com/compose/). The getting started guide isn’t exactly comprehensive, and it can be really frustrating for beginners to get Airflow working. Here are a few things you’ll need to do, and issues you might run into.

Docker Images (like this Airflow one) are built with a [Dockerfile](https://docs.docker.com/engine/reference/builder/), which is sort of like a blueprint for what your Docker Image (and eventual containers) should look like. Dockerfiles will run shell commands, create environment variables, install packages, and all that good stuff you need to create the Container of Your Dreams™️.

A pain point for beginners using this Airflow Docker Image is that a lot of the interesting configuration doesn’t actually happen in [the Dockerfile](https://github.com/puckel/docker-airflow/blob/master/Dockerfile): it happens in [this little script called `entrypoint.sh`](https://github.com/puckel/docker-airflow/blob/master/script/entrypoint.sh). An entrypoint script is just a series of commands that you can have your container run when it starts up, and you put it in the Dockerfile as `ENTRYPOINT [“entrypoint.sh”]`. A bunch of very important variables and configurations are defined there (like Fernet Keys, which we’ll look at in a bit). It also tells the container to immediately run `airflow initdb`, `airflow webserver`, and `airflow scheduler`, so you don’t have to run those manually.

You’re going to run into issues setting up Airflow: there’s no way around it. But you’ll be able to debug much faster if you understand how the Docker Image is being created and what’s being run on your container(s).

***2) Decide on how you want to deploy and test***

The typical structure for building the Airflow Docker Image, which is also how this repo is designed, is two fold:

- A bunch of local files exist that are your “source of truth”
- When Docker Images are built, all of the local data and files are copied over to containers

What this *means* that you’d make edits to any local files like `script/entrypoint.sh` or `config/airflow.cfg`, and then build your image. The Dockerfile will automatically copy all of those local files over, so the new versions will be the only ones that appear in your containers. Since you’ll constantly be running the same [Docker Build](https://docs.docker.com/engine/reference/commandline/build/) and [Docker Run](https://docs.docker.com/engine/reference/run/) commands, it’s convenient to [create a Makefile as a shortcut](https://medium.com/@segal.levi/using-docker-to-explore-airflow-and-other-open-source-projects-e6349ffadf5a).

There are other ways to do this though. If you want to run Airflow on multiple containers, you can use the Docker Compose files included in the repo. For testing and configuration, that might be overkill, but it also can help you avoid some of the issues below.

***3) Create a `COPY` command in the Dockerfile so your DAGs will appear***

When you build your Docker Image using the Dockerfile from `puckel/docker-airflow`, it copies over the local stuff (your `entrypoint.sh` script, your airflow config files, etc.) into the eventual container.

If you build manually and don’t use the included docker-compose files, the Dockerfile in this repo is missing an important COPY statement: you need to copy your `dags` directory into the container too. It’s as simple as adding `COPY dags ${AIRFLOW_HOME}/dags` to your Dockerfile, where `dags` is your local directory and `${AIRFLOW_HOME}/dags` is the target directory in your containers.

***4) Address Fernet Key issues***

When you add Connections to Airflow, it stores your credentials in that internal SQLite database we mentioned above. Airflow encrypts those credentials using [Fernet Encryption](https://cryptography.io/en/latest/fernet/), and you need to generate a key for it to work. You then point Airflow to that key in your `airflow.cfg` file, and all is well. Here’s the way that `puckel/docker-airflow` does it:

- The Fernet Key is generated with a Python command and exported as an environment variable in `entrypoint.sh`
- In the `airflow.cfg` file, the `fernet_key` parameter is set to `$FERNET_KEY`, which is the name of the environment variable exported above

There’s an [open issue](https://github.com/puckel/docker-airflow/issues/290) (created by yours truly) with this process, though: if you build your Docker Image through plain old Docker Build and Docker Run commands, it doesn’t work. The commands as they exist in `entrypoint.sh` aren’t correctly exporting the Fernet Key for whatever reason (I haven’t figured it out yet), and so your Connections will not work without the properly encrypted credentials.

The error message will be `binascii.Error: Incorrect padding`, but that’s actually the wrong error — the key doesn’t exist. Someday I’ll create a pull request to fix the message. Someday.

You can create a simple workaround in the meanwhile by exporting your Fernet Key manually when you create a container (this likely won’t work if you’re using Docker Compose). Just copy the command from `entrypoint.sh` that’s supposed to work — `export FERNET_KEY = python -c “from cryptography.fernet import Fernet; FERNET_KEY = Fernet.generate_key().decode(); print(FERNET_KEY)` — and run it in your container. I run this through a [Docker Exec](https://docs.docker.com/engine/reference/commandline/exec/) command in my Makefile so I don’t need to do it manually each time I build.

*(Note: I’m pretty new to Docker, so there’s a good chance I’ve made some errors above. Send some feedback [on Twitter](https://twitter.com/jGage718)!)*

These are the basics, from the conceptual to the practical parts of deployment. If you’re planning on getting started with Airflow and want more information, there a few other tutorials that will take you deeper in the Airflow lifecycle (past setup). Check out: