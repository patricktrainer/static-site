# Syncing Redshift & PostgreSQL in real-time with Kafka Connect

Created: Feb 21, 2020 12:02 PM
URL: https://blog.insightdatascience.com/from-postgresql-to-redshift-with-kafka-connect-111c44954a6a

![1*pYpurugpdz35peaoDNB93A.png](Syncing%20Redshift%20&%20PostgreSQL%20in%20real-time%20with%20Ka%20a0703025257346c19b5aa7f21cbc8438/1pYpurugpdz35peaoDNB93A.png)

I read about Kafka Connect a while back and always wanted to explore how it worked. It’s a very attractive feature because a significant part of processing data involves taking data from one system to the other. With Kafka becoming a convergence point for many organizations and being used as the backbone of data infrastructure at a lot of companies, Kafka Connect is a great abstraction to make integration with Kafka easy.

Before showing Kafka Connect, we’ll walk through some setup

- Setting up a distributed Kafka cluster
- Setting up a PostgreSQL database on AWS RDS
- Setting up an AWS Redshift instance
- Setting up Confluent’s open source platform

If you’re curious about how Kafka Connect works, I highly recommend reading the [concepts](http://docs.confluent.io/3.1.2/connect/concepts.html) and [architecture and internals](http://docs.confluent.io/3.1.2/connect/design.html) of Kafka Connect on Confluent’s platform documentation.

## Setting up a Kafka cluster

As discussed in a [previous blog](https://blog.insightdatascience.com/ansible-playbooks-for-kafka-and-zookeeper-with-ec2-dynamic-inventory-8f317d4d2bfc), we’ll be using [Ansible playbooks](https://github.com/InsightDataScience/ansible-playbook) to deploy a Kafka cluster on AWS. The yml file to launch EC2 instances is as follows:

We can launch these EC2 instances with the command

```
~$
```

Once the EC2 nodes are ready, we can deploy and start Kafka on these machines with the following two commands:

## Setting up a PostgreSQL instance on AWS RDS

Follow the steps [here](http://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_GettingStarted.CreatingConnecting.PostgreSQL.html#CHAP_GettingStarted.Creating.PostgreSQL) to launch a PostgreSQL instance on AWS RDS. Once the instance has been created, let’s access the database using `[psql](https://www.postgresql.org/docs/9.5/static/app-psql.html)` from one of the EC2 machines we just launched.

To setup psql, we need to SSH into one of the machines for which we need a public IP. We can get the public IPs of the running machines using the command or from the AWS console.

```
~$
```

Let’s SSH into the first machine.

```
~$
```

Once in the EC2 machine, let’s install postgesql-client.

```
~$~$
```

Now, let’s get the endpoint of the PostgreSQL instance from the RDS page and connect to it using `psql`.

```
~$ psql -h kafka-postgres.cvmmptcmh2sg.us-west-2.rds.amazonaws.com <database> <username>
```

Replace the endpoint with your RDS endpoint. You’ll be asked for the password — enter the password and you will be connected to the PostgreSQL database.

## Inserting data into PostgreSQL

Let’s now create a `users` table in PostgreSQL using the following SQL statement:

Let’s insert a few rows in this table.

We can see the data in the table as below:

Now that we have some data in our PostgreSQL table, we can use Kafka Connect to get these rows as messages in a Kafka topic and have a process listening for any inserts/updates on this table.

## Setting up Confluent’s open source platform

Kafka Connect uses the concept of connectors which define where the data should be copied to and from. We’ll be using the JDBC connectors provided in the [Confluent’s open source platform](https://www.confluent.io/product/confluent-platform/). For that, let’s download Confluent’s open source platform on one of the machines using the following script:

## Postgres source configuration

Example configurations for source and sink JDBC connectors for SQLite are present in the directory `/usr/local/confluent/etc/kafka-connect-jdbc`. To ingest data from PostgreSQL we will use the template `source-quickstart-sqlite.properties`. Copy this file and name it `source-postgres.properties`.

```
~$ cp /usr/local/confluent/etc/kafka-connect-jdbc/source-quickstart-sqlite.properties /usr/local/confluent/etc/kafka-connect-jdbc/source-postgres.properties
```

We’ll change the following properties in this file:

- `name`: name for the connector
- `connection.url`: JDBC endpoint for the PostgreSQL database
- `mode`: the JDBC source connector supports various modes, which you can read about [here](http://docs.confluent.io/3.1.2/connect/connect-jdbc/docs/source_connector.html#features). In this case, we will be using the timestamp+increment mode which allows us to capture all updates that result in a unique tuple (id, timestamp).
- `timestamp.column.name`: the column name which has the timestamps
- `incrementing.column.name`: the column which has incremental IDs
- `topic.prefix`: to identify the Kafka topics ingested from PostgreSQL we can specify a prefix value which will be appended to all the table names and the topic name will be prefix+table name

The `source-postgres.properties` should look like this:

## Schema Registry

The JDBC connector from Confluent uses [Schema Registry](http://docs.confluent.io/3.1.2/schema-registry/docs/index.html) to store schema for the messages. A service like schema registry is very useful in tracking and managing scheme updates with proper versioning to make sure downstream processing doesn’t break. Discussing [Schema Registry](http://docs.confluent.io/3.1.2/schema-registry/docs/index.html) is outside the scope of this blog, however, I highly encourage reading about it. We can start schema registry as follows:

```
~$ /usr/local/confluent/bin/schema-registry-start /usr/local/confluent/etc/schema-registry/schema-registry.properties &
```

## Ingest data from PostgreSQL tables to Kafka topics

Let’s create a topic in which we want to consume the updates from PostgreSQL. It is good practice to explicitly create topics so that we can control the number of partitions and replication factor as we may not want to stick with the default values. Our topic name will be `postgres_users`.

```
~$ /usr/local/kafka/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 3 --partitions 1 --topic postgres_users
```

You can check that the topic exists using the following command:

```
~$ /usr/local/kafka/bin/kafka-topics.sh --describe --zookeeper localhost:2181 --topic postgres_users
```

We will be using Kafka Connect in stand-alone mode and we can start the stand-alone job to start consuming data from PostgreSQL table as follows:

```
~$ /usr/local/confluent/bin/connect-standalone /usr/local/confluent/etc/schema-registry/connect-avro-standalone.properties /usr/local/confluent/etc/kafka-connect-jdbc/source-postgres.properties
```

The `jdbc` connector serializes the data using Avro and we can use the Avro console consumer provided by Confluent to consume these messages from Kafka topic. You can run the following command on the Kafka broker that has the Confluent platform and Schema Registry running.

```
~$ sudo /usr/local/confluent/bin/kafka-avro-console-consumer --new-consumer --bootstrap-server localhost:9092 --topic postgres_users --from-beginning
```

If you want to consume this topic from a different broker, setup the Confluent platform on that broker, start Schema Registry and you should be able to use the above command. The messages on the console should look as follows:

You can check that these are all the rows in your PostgreSQL table. Try inserting another row or updating an existing row while having this console consumer running. You’ll see that the updates from PostgreSQL will be captured in this topic.

## Setting up Redshift

Setup a Redshift instance by following the steps [here](http://docs.aws.amazon.com/redshift/latest/gsg/rs-gsg-launch-sample-cluster.html). Once the Redshift instance is ready, get the endpoint from the Redshift dashboard.

We can use the `psql` client to connect to Redshift as follows:

```
~$ psql -h kafka-redshift.cniqeoxrupxt.us-west-2.redshift.amazonaws.com -p 5439 <DATABASE> <USERNAME>
```

Replace the Redshift endpoint templates with your actual Redshift endpoint. You will be prompted for the password. Once connected to Redshift, let’s create a table with the same name as the Kafka topic from which we want to write the messages to Redshift. The SQL statement to create the Redshift table is:

## Download the Redshift JDBC driver

The Confluent JDBC connector doesn’t ship with a Redshift JDBC driver so we need to download it. You can use the following script to download the driver and place it in the path where the connect-standalone process can find it.

## Redshift sink properties file

We will use the template sink file — `/usr/local/confluent/etc/kafka-connect-jdbc/sink-quickstart-sqlite.properties` — to create the properties file to use Redshift as a sink. Copy this template file to a file named `sink-redshift.properties`. Change the following properties:

- `name`: name for the connector
- `topics`: Kafka topic to write data from
- `connection.url`: JDBC endpoint for Redshift
- `auto.create`: it is `true` by default and we will change it to `false` as we’ve already created the table in Redshift that this data should be written to. It is good practice to create the table yourself and control the schema explicitly.

The `sink-redshift.properties` should look as follows:

## Send messages from the Kafka topic to Redshift

We are all set to have messages from the Kafka topic write to the Redshift table. Connect standalone process can take multiple connectors at a time — they just need to be space separated config files. Stop the previous connect stand-alone job and start a new one, this time specifying config files for both PostgreSQL as a source and Redshift as a sink. You can use the following statement:

```
~$ /usr/local/confluent/bin/connect-standalone /usr/local/confluent/etc/schema-registry/connect-avro-standalone.properties /usr/local/confluent/etc/kafka-connect-jdbc/source-postgres.properties /usr/local/confluent/etc/kafka-connect-jdbc/sink-redshift.properties
```

With this running, connect to your Redshift cluster from any machine using `psql` and query the `postgres_users` table. You should see the following rows, though not necessarily in this order.

Keep the Connect job running and insert/update a row in PostgreSQL. You will see this information propagate to the Kafka topic, and from the topic to the Redshift table.

## Conclusion

In this blog, we saw how we can use different systems as sources and sinks for Kafka. There are a lot of other [connectors available](https://www.confluent.io/product/connectors/) making various systems integrable with Kafka making Kafka the go-to choice to transport data in a centralized way throughout the infrastructure.

*The examples here are only for prototyping purposes and haven’t been tested in any production setup. There are a few things these connectors don’t do yet like throw an exception when the topic specified doesn’t exist, etc. To use these connectors in production, make sure you’ve tested the setup comprehensively.*