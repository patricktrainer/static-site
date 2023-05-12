# Quick guide: How to run Apache Airflow with docker-compose

Created: Jan 30, 2020 4:02 PM
Notes: https://www.notion.so/Airflow-f155982af8c341babd96e1b6b40c4358
URL: https://medium.com/@xnuinside/quick-guide-how-to-run-apache-airflow-cluster-in-docker-compose-615eb8abd67a

![1*okeHnslEJpFEbpMuGGCpIA.png](Quick%20guide%20How%20to%20run%20Apache%20Airflow%20with%20docker-%20a0f836899b124615ac4b29f8568d5e82/1okeHnslEJpFEbpMuGGCpIA.png)

**UPD from 29.11.2019: versions update to 1.10.6**

**UPGRADE UPPER 1.10.5 be AWARE:** You need to define ‘**default_pool**’ for task instances and set number slots to it, for example, 100. This was not needed previous because of **default_poll** was exist by default. **But now you need to create it manually**. So just go to UI, **Admin -> Pools** ([http://localhost:8080/admin/pool/](http://localhost:8080/admin/pool/)) **and press *Create***. Create pool with name ‘**default_pool**’ and slots, for example **100**.

This article expects that you already know that is [**Apache Airflow**](https://airflow.readthedocs.io/en/stable/) andwhy is it needed. And you are here because you want an easy way how to use and develop workflow in a local environment. What can be designed close to real production or you just don’t want to run the Apache Airflow global.

So this is a very simple and very quick guide on how to wake up **Apache Airflow** with **[docker-compose](https://docs.docker.com/compose/)** and work with it. I’m working with macOS, so all stuff worked on it 100%, I think, that same must be near the truth for Linux users also.

We will create a docker-compose file with:

- airflow webserver
- airflow scheduler (with LocalExecutor)
- PostgreSQL DB (we will use it as DB for Airflow)

For **PostgreSQL**, we will use the official docker image: [https://hub.docker.com/_/postgres/](https://hub.docker.com/_/postgres/) version 9.6.14, for **Apache** **Airflow**: [https://hub.docker.com/r/puckel/docker-airflow/](https://hub.docker.com/r/puckel/docker-airflow/) version 1.10.6 (note: we will switch to use official docker image as soon as it will be released, now we can just check AIP and wait, or participate if you can and want in process of creation).

At the start, for quick development we will use one DAG folder that we will share between airflow scheduler and airflow webserver, so you will not need to rebuild and re-run server each time when you want to add dags. We will use **volumes** for this.

## **Prerequisites**

At the first step, you will need a **Docker** (with support version 3 of docker-compose), if for some reason in 2019 you still does not install it — please ‘google’ guides how to install it on your OS. Or use official guides: [https://docs.docker.com/install/linux/docker-ce/ubuntu/](https://docs.docker.com/install/linux/docker-ce/ubuntu/) (Ubuntu) and [https://docs.docker.com/docker-for-mac/install/](https://docs.docker.com/docker-for-mac/install/) (Mac)

**Step 1. Prepare airflow.cfg and Dockerfile**

To be able to work with PostgreSQL DB we need to change airflow.cfg (if you don’t have airflow.cfg, you can take it here: [https://github.com/xnuinside/airflow_in_docker_compose/blob/master/airflow.cfg](https://github.com/xnuinside/airflow_in_docker_compose/blob/master/airflow.cfg)) .

We need to modify **`sql_alchemy_conn =`** variable from sqlite-usage to PostgreSQL.

So you will have in airflow.cfg:

```
sql_alchemy_conn = postgresql+psycopg2://$your_db_user:$your_db_password@$your_postgres_db_host:$postgres_port/$db_namein my example it will be:sql_alchemy_conn = postgresql+psycopg2://airflow:airflow@postgres:5432/airflow
```

To be honest, we do not need to modify separate airflow.cfg and put inside docker image file with COPY. Because with puckle image that we use, you can just set DB params with environment variables in docker-compose.yml (see sources how to do this —[https://github.com/puckel/docker-airflow/blob/master/script/entrypoint.sh](https://github.com/puckel/docker-airflow/blob/master/script/entrypoint.sh)). But I add this way ‘with separate cfg file’ to have more customization ways. So just add/overwrite all the things that you need in Dockerfile — and be happy.

Also, because, puckle image has entrypoint.sh script with parse variables and cfg changing based on this variables — **we will overwrite entrypoint in docker-compose file**, to be sure, that we start pure airflow without any variables and changes before the start.

1.1 Prepare the main folder (in git source is called **airflow_in_docker_compose**) all files will be placed inside it.

1.2 Inside **main_folder** put airflow.cfg file with modified **‘sql_alchemy_conn =’** variable (was described upper).

1.3 Next, create a file with name **Dockerfile** (this is a default name for docker files to build images, let use it)

**In Dockerfile:**

```
FROM/RUN--ENVAIRFLOW_HOME///COPY/////
```

Short description: **FROM** — define a base image that we use to create our image, **ENV** — define environment variables in an image, **COPY** — copy file from the local path to an image, **RUN** — run command.

1.4 Also, create a file with name docker-compose.yml and leave it empty now.

After, you got a structure:

```
…/main_folder  — airflow.cfg — Dockerfile - docker-compose.yml
```

**Step 2. Prepare docker-compose file**

2.1 Now time to fill docker-compose.yml with:

```
versionservicespostgresimagecontainer_nameenvironmentportsvolumescomment initdb after you will have use it at first runinitdb:build:entrypoint:depends_on:webserverbuildrestartdepends_onvolumesportsentrypointhealthchecktestintervaltimeoutretriesschedulerbuildrestartdepends_onvolumesentrypointhealthchecktestintervaltimeoutretries
```

What is health check you can read here:[https://docs.docker.com/engine/reference/builder/#healthcheck](https://docs.docker.com/engine/reference/builder/#healthcheck). But, you can remove this section, all will also work correctly.

**Pay attention to volumes:**

```
volumes
```

and

```
volumes
```

The path at the left part of volumes before ‘:’ **./airflow_files/dags** and **./data/postgres** are the folders in your local machine (not in docker image!!!) that will be shared to docker images as a path from the right side.

So, if you will put a file in main_folder/airflow/dags (**‘.’** — mean current work dir **where docker-compose.yaml is placed,** so this is **main_folder**) it will be shown in Airflow images in /usr/local/airflow/dags, so Airflow webserver and Airflow Scheduler will see it.

You can also add volumes for **airflow** **plugins folder** if you need it**.**

2.2 Save docker-compose.yml.

**Step 3. Up docker-compose cluster.**

At first time and each time when you will clean your Postgres data folder (in our example — **./data/postgres** directory), you need to run postgres service in a separate terminal window and wait till it creates a database and init data folder. This will be enough for this tutorial, but…

If you don’t want to do it with way, you can spend a little time and create a .sh script to put in docker-compose airflow services wait till DB will not create, that is this you can see, for example, here: [https://github.com/vishnubob/wait-for-it](https://github.com/vishnubob/wait-for-it) but of course you need to modify sh to check is DB available to use or not.

**3.1 Let’s run:**

```
main_folderdocker-compose up postgres
```

3.1.1 after that in another terminal window run initdb (we need it only once if we clean up DB and start all from scratch)

```
docker-compose up initdb
```

3.2 After that run **in another terminal window:**

```
docker-compose up scheduler webserver
```

As you see postgres, schedule and webserver — names of our services, that we defined in docker-compose.yml

On next runs you can simply use (don’t forget to comment initdb service in docker-compose.yml):

```
docker-compose up
```

3.3 Now enter a UI to check at **[http://localhost:8080](http://localhost:8080/)**, that all run successfully. It must be empty:

**Step 4. Add a DAG.**

We will use to test our infrastructure simple BashOperator DAG from Apache Airflow examples.

4.1 Take it here (you need the whole file as a DAG):

And copy it in your dags folder, that was defined in the **volumes section of docker-compose file**

So, you got a structure of the main folder:

```
…/main_folder  — airflow.cfg — Dockerfile - docker-compose.yml airflow_files/ dags/ - example_bash_operator.py
```

4.2 Wait for 10–15 sec and check the UI, refresh it and wait for more if it still empty.

You must see your new DAG in UI

**Step 5. Run DAG and test it**

Now, switch Dag from the paused state (change ‘Off’ to ‘On’) and wait few seconds. Because it has schedule and start_date in past it will pick up by Airflow Scheduler auto and run.

In UI you will have green DAG Runs:

And also you can check the console and see something like this on it with information about the run

What is next?