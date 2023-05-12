# ETL and ELT design patterns for lake house architecture using Amazon Redshift: Part 2 | AWS Big Data Blog

Created: Jan 28, 2020 8:42 PM
Tags: Data
URL: https://aws.amazon.com/blogs/big-data/etl-and-elt-design-patterns-for-lake-house-architecture-using-amazon-redshift-part-2/?nc1=b_rp

Part 1 of this multi-post series, [ETL and ELT design patterns for lake house architecture using Amazon Redshift: Part 1](https://aws.amazon.com/blogs/big-data/etl-and-elt-design-patterns-for-lake-house-architecture-using-amazon-redshift-part-1/), discussed common customer use cases and design best practices for building ELT and ETL data processing pipelines for data lake architecture using [Amazon Redshift Spectrum](https://docs.aws.amazon.com/redshift/latest/dg/c-getting-started-using-spectrum.html), [Concurrency Scaling](https://docs.aws.amazon.com/redshift/latest/dg/concurrency-scaling.html), and recent support for data lake export.

This post shows you how to get started with a step-by-step walkthrough of a few ETL and ELT design patterns of [Amazon Redshift](http://aws.amazon.com/redshift) using AWS sample datasets.

## Prerequisites

Before getting started, make sure that you meet the following prerequisites:

1. This post uses two publicly available AWS sample datasets from the US-West-2 (Oregon) Region. Use the US-West-2 (Oregon) Region for your test run to reduce cross-region network latency and cost due to the data movement.
2. You have an AWS account in the same Region.
3. You have the `AdministratorAccess` policy granted to your AWS account (for production, you should restrict this further).
4. You have an existing Amazon S3 bucket named `eltblogpost` in your data lake to store unloaded data from Amazon Redshift. Because bucket names are unique across AWS accounts, replace `eltblogpost` with your unique bucket name as applicable in the sample code provided.
5. You have [AWS CLI](https://aws.amazon.com/cli/) installed and configured to use with your AWS account.
6. You have an IAM policy named `redshift-elt-test-s3-policy` with the following read and write permissions for the Amazon S3 bucket named `eltblogpost`:  

    ```
    { "Version": "2012-10-17", "Statement": [ { "Action": [ "s3:GetBucketLocation", "s3:GetObject", "s3:ListBucket", "s3:ListBucketMultipartUploads", "s3:ListMultipartUploadParts", "s3:AbortMultipartUpload", "s3:PutObject", "s3:DeleteObject" ], "Resource": [ "arn:aws:s3:::eltblogpost", "arn:aws:s3:::eltblogpost/*" ], "Effect": "Allow" } ] }
    ```

7. You have an IAM policy named `redshift-elt-test-sampledata-s3-read-policy` with read only permissions for the Amazon S3 bucket named `awssampledbuswest2`, hosting the sample data used for this walkthrough.  

    ```
    { "Version": "2012-10-17", "Statement": [ { "Effect": "Allow", "Action": [ "s3:Get*", "s3:List*" ], "Resource": [ "arn:aws:s3:::awssampledbuswest2", "arn:aws:s3:::awssampledbuswest2/*" ] } ] }
    ```

8. You have an IAM role named `redshift-elt-test-role` that has a trust relationship with [redshift.amazonaws.com](http://redshift.amazonaws.com/) and [glue.amazonaws.com](http://glue.amazonaws.com/) and the following IAM policies (for production, you should restrict this further as needed):  
    - `redshift-elt-test-s3-policy`
    - `redshift-elt-test-sampledata-s3-read-policy`
    - `AWSGlueServiceRole`
    - `AWSGlueConsoleFullAccess`
9. Make a note of the ARN for `redshift-elt-test-role` IAM role.
10. You have an existing Amazon Redshift cluster with the following parameters:  
    - Cluster name as `rseltblogpost`.
    - Database name as `rselttest`.
    - Four dc2.large nodes.
    - An associated IAM role named `redshift-elt-test-role`.
    - A publicly available endpoint.
    - A cluster parameter group named `eltblogpost-parameter-group`, which you use to change the Concurrency Scaling
    - Cluster workload management set to manual.
11. You have SQL Workbench/J (or another tool of your choice) and can connect successfully to the cluster.
12. You have an EC2 instance in the same Region with PostgreSQL client CLI (psql) and can connect successfully to the cluster.
13. You have an [AWS Glue](https://aws.amazon.com/glue/) catalog database named `eltblogpost` as the metadata catalog for [Amazon Athena](http://aws.amazon.com/athena) and Redshift Spectrum queries.

## Loading data to Amazon Redshift local storage

This post uses the Star Schema Benchmark (SSB) dataset. It is provided publicly in an S3 bucket (`s3://awssampledbuswest2/ssbgz/`), which any authenticated AWS user with access to [Amazon S3](http://aws.amazon.com/s3) can access.

To load data to Amazon Redshift local storage, complete the following steps:

1. Connect to the cluster from the SQL Workbench/J.
2. Execute the CREATE TABLE statements from the [Github repo](https://github.com/aws-samples/aws-blog-redshift-datalake-etl-elt-patterns/blob/master/ssb/ssb-ddl.sql) from your SQL Workbench/J to create tables from the SSB dataset. The following diagram shows the list of tables.

    ![ETL%20and%20ELT%20design%20patterns%20for%20lake%20house%20archite%20a7ad18bd8ea843fc888aa1d3d5246856/ETLandELTRedshiftPart2_1.png](ETL%20and%20ELT%20design%20patterns%20for%20lake%20house%20archite%20a7ad18bd8ea843fc888aa1d3d5246856/ETLandELTRedshiftPart2_1.png)

3. Execute the COPY statements from the [Github repo](https://github.com/aws-samples/aws-blog-redshift-datalake-etl-elt-patterns/blob/master/ssb/ssb-copy.sql). This step loads data into the tables you created using the sample data available in `s3://awssampledbuswest2/ssbgz/`. Remember to replace your IAM role ARN noted previously.
4. To verify that each table loaded correctly, run the following commands:    

    ```
    select count(*) from LINEORDER; select count(*) from PART; select count(*) from CUSTOMER; select count(*) from SUPPLIER; select count(*) from DWDATE;
    ```

    The following results table shows the number of rows for each table in the SSB dataset:

    ```
    Table Name Record Count LINEORDER 600,037,902 PART 1,400,000 CUSTOMER 3,000,000 SUPPLIER 1,000,000 DWDATE 2,556
    ```

In addition to the record counts, you can also check for a few sample records from each table.

## Performing ELT and ETL using Amazon Redshift and unload to S3

The following are the high-level steps for this walkthrough:

1. You are looking to pre-aggregate some commonly asked measures by your end-users on the point of sales (POS) data you loaded in Amazon Redshift local storage.
2. You want to then unload the aggregated data from Amazon Redshift to your data lake (S3) in an open and analytics optimized and compressed Parquet file format. You also want to consider an optimized partitioning for the unloaded data in your data lake to help with the end-user query performance and eventually lower cost.
3. You want to query the unloaded data from your data lake with Redshift Spectrum. You also want to share the data with other AWS services such as Athena with its pay-per-use and serverless ad hoc and on-demand query model, AWS Glue and [Amazon EMR](http://aws.amazon.com/emr) for performing ETL operations on the unloaded data and data integration with your other datasets (such as ERP, finance, or third-party data) stored in your data lake, and [Amazon SageMaker](https://aws.amazon.com/documentation/sagemaker/) for machine learning.

Complete the following steps:

1. To compute the necessary pre-aggregates, execute the following three ELT queries available on the [Github repo](https://github.com/aws-samples/aws-blog-redshift-datalake-etl-elt-patterns/blob/master/ssb/ssb-elt.sql) from your SQL Workbench/J:  
    - **ELT Query 1** – This query summarizes the revenue by manufacturer, category, and brand per month per year per supplier region.
    - **ELT Query 2** – This query summarizes the revenue by brand per month per year by supplier region and city.
    - **ELT Query 3** – This query drills down in time by customer city, supplier city, month, and year.
2. To unload the aggregated data to S3 with Parquet file format and proper partitioning to help with the access patterns of the unloaded data in the data lake, execute the three UNLOAD queries available on the [Github repo](https://github.com/aws-samples/aws-blog-redshift-datalake-etl-elt-patterns/blob/master/ssb/ssb-unload.sql) from your SQL Workbench/J. To use Redshift Spectrum for querying the unloaded data, you need the following:  
    - An Amazon Redshift cluster and a SQL client (SQL Workbench/J or another tool of your choice) that can connect to your cluster and execute SQL commands. The cluster and the data files in S3 must be in the same Region.
    - An external schema in Amazon Redshift that references a database in the external data catalog and provides the IAM role ARN that authorizes your cluster to access S3 on your behalf. It is a best practice to have an external data catalog in AWS Glue.You are now ready to create an AWS Glue crawler.
3. From AWS CLI, run the following code (replace *<Your AWS Account>*):   

    ```
    aws glue create-crawler --cli-input-json file://mycrawler.json --region us-west-2
    ```

    ```
    Where the file mycrawler.json contains: { "Name": "eltblogpost_redshift_spectrum_etl_elt_glue_crawler", "Role": "arn:aws:iam::<Your AWS Account>:role/redshift-elt-test-role", "DatabaseName": "eltblogpost", "Description": "", "Targets": { "S3Targets": [ { "Path": "s3://eltblogpost/unload_parquet/monthly_revenue_by_region_manufacturer_category_brand" }, { "Path": "s3://eltblogpost/unload_parquet/monthly_revenue_by_region_city_brand" }, { "Path": "s3://eltblogpost/unload_parquet/yearly_revenue_by_city" } ] } }
    ```

    You can also schedule the crawler to run periodically based on your use case. For example, you can schedule the crawler every 35 minutes to keep the AWS Glue catalog tables up to date with the data being unloaded every 30 minutes. However, this post does not configure any scheduling.

4. After you create the AWS Glue crawler, run it manually from AWS CLI with the following command:  

    ```
    aws glue start-crawler --name "eltblogpost_redshift_spectrum_etl_elt_glue_crawler" --region us-west-2
    ```

5. When the AWS Glue crawler run is complete, go to the AWS Glue console to see the following three AWS Glue catalog tables under the database `eltblogpost`:  
    - `monthly_revenue_by_region_manufacturer_category_brand`
    - `monthly_revenue_by_region_city_brand`
    - `yearly_revenue_by_city`
6. Now that you have an external data catalog in AWS Glue named `etlblogpost`, create an external schema in the persistent cluster named `eltblogpost` using the following SQL from your SQL Workbench/J (replace *<Your AWS Account>*):  

    ```
    create external schema spectrum_eltblogpost from data catalog database 'eltblogpost' iam_role 'arn:aws:iam::<Your AWS Account>:role/redshift-elt-test-role' create external database if not exists;
    ```

    Using Spectrum, you can now query the three AWS Glue catalog tables you set up earlier.

7. Go to SQL Workbench/J and run the following sample queries:  
    - Top 10 brands by category and manufacturer contributing to revenue for the region `AFRICA` for the year of 1992 and month of March:

        ```
        SELECT brand, category, manufacturer, revenue from "spectrum_eltblogpost"."monthly_revenue_by_region_manufacturer_category_brand" where year = '1992' and month = 'March' and supplier_region = 'AFRICA' order by revenue desc limit 10; brand | category | manufacturer | revenue ----------+----------+--------------+----------- MFGR#1313 | MFGR#13 | MFGR#1 | 5170356068 MFGR#5325 | MFGR#53 | MFGR#5 | 5106463527 MFGR#3428 | MFGR#34 | MFGR#3 | 5055551376 MFGR#2425 | MFGR#24 | MFGR#2 | 5046250790 MFGR#4126 | MFGR#41 | MFGR#4 | 5037843130 MFGR#219 | MFGR#21 | MFGR#2 | 5018018040 MFGR#159 | MFGR#15 | MFGR#1 | 5009626205 MFGR#5112 | MFGR#51 | MFGR#5 | 4994133558 MFGR#5534 | MFGR#55 | MFGR#5 | 4984369900 MFGR#5332 | MFGR#53 | MFGR#5 | 4980619214
        ```

    - Monthly revenue for the region `AMERICA` for the year 1995 across all brands:

        ```
        SELECT month, sum(revenue) revenue FROM "spectrum_eltblogpost"."monthly_revenue_by_region_city_brand" where year = '1992' and supplier_region = 'AMERICA' group by month; month | revenue ----------+-------------- April | 4347703599195 January | 4482598782080 September | 4332911671240 December | 4489411782480 May | 4479764212732 August | 4485519151803 October | 4493509053843 June | 4339267242387 March | 4477659286311 February | 4197523905580 November | 4337368695526 July | 4492092583189
        ```

    - Yearly revenue for supplier city `ETHIOPIA` 4 for the years 1992–1995 and month of December:

        ```
        SELECT year, supplier_city, sum(revenue) revenue FROM "spectrum_eltblogpost"."yearly_revenue_by_city" where supplier_city in ('ETHIOPIA 4') and year between '1992' and '1995' and month = 'December' group by year, supplier_city order by year, supplier_city; year | supplier_city | revenue -----+---------------+------------ 1992 | ETHIOPIA 4 | 91006583025 1993 | ETHIOPIA 4 | 90617597590 1994 | ETHIOPIA 4 | 92015649529 1995 | ETHIOPIA 4 | 89732644163
        ```

When the data is in S3 and cataloged in the AWS Glue catalog, you can query the same catalog tables using Athena, AWS Glue, Amazon EMR, Amazon SageMaker, [Amazon QuickSight](https://aws.amazon.com/quicksight/), and many more AWS services that have seamless integration with S3.

## Accelerating ELT and ETL using Redshift Spectrum and unload to S3

Assume that you need to pre-aggregate a set of commonly requested metrics from your end-users on a large dataset stored in the data lake (S3) cold storage using familiar SQL and unload the aggregated metrics in your data lake for downstream consumption.

The following are the high-level steps for this walkthrough:

1. This is a batch workload that requires standard SQL joins and aggregations on a fairly large volume of relational and structured data. You want to use the power of Redshift Spectrum to perform the required SQL transformations on the data stored in S3 and unload the transformed results back to S3.
2. You want to query the unloaded data from your data lake using Redshift Spectrum if you have an existing cluster, Athena with its pay-per-use and serverless ad hoc and on-demand query model, AWS Glue and Amazon EMR for performing ETL operations on the unloaded data and data integration with your other datasets in your data lake, and Amazon SageMaker for machine learning.

Because Redshift Spectrum allows you to query the data directly from your data lake without needing to load into Amazon Redshift local storage, you can spin up a short-lived cluster to perform ELT at a massive scale using Redshift Spectrum and terminate the cluster when the work is complete. You can automate spinning up and terminating the short-lived cluster using [AWS CloudFormation](https://aws.amazon.com/cloudformation/). That way, you only pay for the duration in which your Amazon Redshift clusters serve your workloads. A short-lived cluster can also avoid overloading the current persistent cluster serving interactive queries from live users. For this post, use your existing cluster `rseltblogpost`.

This post uses a publicly available sample dataset named `tickit` provided by AWS, which any authenticated AWS user with access to S3 can access:

- **Sales** – s3://awssampledbuswest2/tickit/spectrum/sales/
- **Event** – s3://awssampledbuswest2/tickit/allevents_pipe.txt
- **Date** – s3://awssampledbuswest2/tickit/date2008_pipe.txt
- **Users** – s3://awssampledbuswest2/tickit/allusers_pipe.txt

It is a best practice of Redshift Spectrum for performance reasons to load the dimension tables in the local storage of your short-lived cluster and use an external table for the fact table `Sales`.

Complete the following steps:

1. Connect to the cluster from the SQL Workbench/J.To use Redshift Spectrum for querying data from data lake (S3), you need to have the following:  
    - An Amazon Redshift cluster and a SQL client (SQL Workbench/J or another tool of your choice) that can connect to your cluster and execute SQL commands. The cluster and the data files in S3 must be in the same Region.
    - An external schema in Amazon Redshift that references a database in the external data catalog and provides the IAM role ARN that authorizes your cluster to access S3 on your behalf. It is a best practice to have an external data catalog in AWS Glue.
    - An AWS Glue catalog database named `eltblogpost` that you already created.
    - An external schema in your Redshift cluster named `spectrum_eltblogpost` that you already created.
2. Execute the SQL available on the [Github repo](https://github.com/aws-samples/aws-blog-redshift-datalake-etl-elt-patterns/blob/master/tickit/tickit-ddl-sales-external.sql) to create an external table named `sales` in the same external schema named `spectrum_eltblogpost`. As shown in the previous section, you can also use an AWS Glue crawler to create the external table.
3. Execute the SQLs available on the [Github repo](https://github.com/aws-samples/aws-blog-redshift-datalake-etl-elt-patterns/blob/master/tickit/tickit-ddl-dimensions.sql) to create the dimension tables to load the data into Amazon Redshift local storage for Redshift Spectrum performance best practices.
4. Execute the COPY statements available on the [Github repo](https://github.com/aws-samples/aws-blog-redshift-datalake-etl-elt-patterns/blob/master/tickit/tickit-copy-dimensions.sql) to load the dimension tables using the sample data available in `s3://awssampledbuswest2/tickit/`. Replace the IAM role ARN with the IAM role ARN you noted earlier, which is associated with your cluster.
5. To verify that each table has the correct record count, execute the following commands:    

    ```
    select count(*) from date; select count(*) from users; select count(*) from event; select count(*) from spectrum_eltblogpost.sales;
    ```

    The following results table shows the number of rows for each table in the `tickit` dataset:

    ```
    Table Name Record Count DATE 365 USERS 49,990 EVENT 8,798 spectrum_eltblogpost.sales 172,456
    ```

    In addition to the record counts, you can also check for a few sample records from each table.

6. To compute the necessary pre-aggregates, execute the following three ELT queries available on the [Github repo](https://github.com/aws-samples/aws-blog-redshift-datalake-etl-elt-patterns/blob/master/tickit/tickit-elt.sql) from your SQL Workbench/J:  
    - **ELT Query 1** – Total quantity sold on a given calendar date.
    - **ELT Query 2** – Total quantity sold to each buyer.
    - **ELT Query 3** – Events in the 99.9 percentile in terms of all-time gross sales.
7. To unload the aggregated data to S3 with Parquet file format and proper partitioning to help with the access patterns of the unloaded data in the data lake, execute the three UNLOAD queries available on the [Github repo](https://github.com/aws-samples/aws-blog-redshift-datalake-etl-elt-patterns/blob/master/tickit/tickit-unload.sql) from your SQL Workbench/J.
8. To use Redshift Spectrum for querying the unloaded data, you can either create a new AWS Glue crawler or modify the previous crawler named `eltblogpost_redshift_spectrum_etl_elt_glue_crawler`. Update the existing crawler using the following code from AWS CLI (replace *<Your AWS Account>*):   

    ```
    aws glue update-crawler --cli-input-json file://mycrawler.json --region us-west-2
    ```

    ```
    Where the file mycrawler.json contains: { "Name": "eltblogpost_redshift_spectrum_etl_elt_glue_crawler", "Role": "arn:aws:iam::<Your AWS Account>:role/redshift-elt-test-role", "DatabaseName": "eltblogpost", "Description": "", "Targets": { "S3Targets": [ { "Path": "s3://eltblogpost/unload_parquet/monthly_revenue_by_region_manufacturer_category_brand" }, { "Path": "s3://eltblogpost/unload_parquet/monthly_revenue_by_region_city_brand" }, { "Path": "s3://eltblogpost/unload_parquet/yearly_revenue_by_city" }, { "Path": "s3://eltblogpost/unload_parquet/total_quantity_sold_by_date" }, { "Path": "s3://eltblogpost/unload_parquet/total_quantity_sold_by_buyer_by_date" }, { "Path": "s3://eltblogpost/unload_parquet/total_price_by_eventname" } ] } }
    ```

9. After you create the crawler successfully, run it manually from AWS CLI with the following command:  

    ```
    aws glue start-crawler --name "eltblogpost_redshift_spectrum_etl_elt_glue_crawler" --region us-west-2
    ```

10. When the crawler run is complete, go to the AWS Glue console. The following additional catalog tables are in the catalog database `eltblogpost`:  
    - total_quantity_sold_by_date
    - total_quantity_sold_by_buyer_by_date
    - total_price_by_eventname
11. Using Spectrum, you can now query the three preceding catalog tables. Go to SQL Workbench/J and run the following sample queries:  
    - 
        - Top 10 days for quantities sold in February and March 2008:

            ```
            SELECT caldate, total_quantity FROM "spectrum_eltblogpost"."total_quantity_sold_by_date" where caldate between '2008-02-01' and '2008-03-30' order by total_quantity desc limit 10; caldate | total_quantity -----------+--------------- 2008-02-20 | 1170 2008-02-25 | 1146 2008-02-19 | 1145 2008-02-24 | 1141 2008-03-26 | 1138 2008-03-22 | 1136 2008-03-17 | 1129 2008-03-08 | 1129 2008-02-16 | 1127 2008-03-23 | 1121
            ```

        - Top 10 buyers for quantities sold in February and March 2008:

            ```
            SELECT firstname,lastname,total_quantity FROM "spectrum_eltblogpost"."total_quantity_sold_by_buyer_by_date" where caldate between '2008-02-01' and '2008-03-31' order by total_quantity desc limit 10; firstname | lastname | total_quantity ----------+------------+--------------- Laurel | Clay | 9 Carolyn | Valentine | 8 Amelia | Osborne | 8 Kai | Gill | 8 Gannon | Summers | 8 Ignacia | Nichols | 8 Ahmed | Mcclain | 8 Amanda | Mccullough | 8 Blair | Medina | 8 Hadley | Bennett | 8
            ```

        - Top 10 event names for total price:

            ```
            SELECT eventname, total_price FROM "spectrum_eltblogpost"."total_price_by_eventname" order by total_price desc limit 10; eventname | total_price ---------------------+------------ Adriana Lecouvreur | 51846.00 Janet Jackson | 51049.00 Phantom of the Opera | 50301.00 The Little Mermaid | 49956.00 Citizen Cope | 49823.00 Sevendust | 48020.00 Electra | 47883.00 Mary Poppins | 46780.00 Live | 46661.00
            ```

After the data is in S3 and cataloged in the AWS Glue catalog, you can query the same catalog tables using Amazon Athena, AWS Glue, Amazon EMR, Amazon SageMaker, Amazon QuickSight, and many more AWS services that have seamless integration with S3.

## Scaling ELT and unload running in parallel using Concurrency Scaling

Assume that you have a mixed workload under concurrency when the UNLOAD queries and the ELT jobs run in parallel in your cluster with Concurrency Scaling turned on. When Concurrency Scaling is enabled, Amazon Redshift automatically adds additional cluster capacity when you need to process an increase in concurrent read queries including UNLOAD queries. By default, Concurrency Scaling mode is turned off for your cluster. In this post, you enable the Concurrency Scaling mode for your cluster.

Complete the following steps:

1. Go to your cluster parameter group named `eltblogpost-parameter-group` and complete the following:  
    - Update `max_concurrency_scaling_clusters` to `5`.
    - Create a new queue named `Queue 1` with Concurrency Scaling mode set to `Auto` and a query group named `unload_query` for the UNLOAD jobs in the next steps.
2. After you make these changes, reboot your cluster for the changes to take effect.
3. For this post, use **psql** client to connect to your cluster `rseltblogpost` from the EC2 instance that you set up earlier.
4. Open an SSH session to your EC2 instance and copy the nine files as shown below from the concurrency folder in the [Github repo](https://github.com/aws-samples/aws-blog-redshift-datalake-etl-elt-patterns/tree/master/concurrency) to `/home/ec2-user/eltblogpost/` in your EC2 instance.

    ![ETL%20and%20ELT%20design%20patterns%20for%20lake%20house%20archite%20a7ad18bd8ea843fc888aa1d3d5246856/ETLandELTRedshiftPart2_2.png](ETL%20and%20ELT%20design%20patterns%20for%20lake%20house%20archite%20a7ad18bd8ea843fc888aa1d3d5246856/ETLandELTRedshiftPart2_2.png)

5. Review the `concurrency-elt-unload.sh` script that runs the following eight jobs in parallel:  
    - An ELT script for SSB dataset, which kicks off one query at a time.
    - An ELT script for the `tickit` dataset, which kicks off one query at a time.
    - Three unload queries for the SSB datasets kicked off in parallel.
    - Three unload queries for the `tickit` datasets kicked off in parallel.
6. Run the `concurrency-elt-unload.sh` While the script is running, you will see the following sample output: The following are the response times taken by the script:  

    ![ETL%20and%20ELT%20design%20patterns%20for%20lake%20house%20archite%20a7ad18bd8ea843fc888aa1d3d5246856/ETLandELTRedshiftPart2_3.png](ETL%20and%20ELT%20design%20patterns%20for%20lake%20house%20archite%20a7ad18bd8ea843fc888aa1d3d5246856/ETLandELTRedshiftPart2_3.png)

    ```
    real 2m40.245s user 0m0.104s sys 0m0.000s
    ```

7. Run the following query to validate that some of the UNLOAD queries ran in the Concurrency Scaling clusters (look for “`which_cluster = Concurrency Scaling`” in the query output below):  

    ```
    SELECT query, Substring(querytxt,1,90) query_text, starttime starttime_utc, (endtime-starttime)/(1000*1000) elapsed_time_secs, case when aborted= 0 then 'complete' else 'error' end status, case when concurrency_scaling_status = 1 then 'Concurrency Scaling' else 'Main' end which_cluster FROM stl_query WHERE database = 'rselttest' AND starttime between '2019-10-20 22:53:00' and '2019-10-20 22:56:00’ AND userid=100 AND querytxt NOT LIKE 'padb_fetch_sample%' AND (querytxt LIKE 'create%' or querytxt LIKE 'UNLOAD%') ORDER BY query DESC;
    ```

    See the following output from the query:

    ![ETL%20and%20ELT%20design%20patterns%20for%20lake%20house%20archite%20a7ad18bd8ea843fc888aa1d3d5246856/ETLandELTRedshiftPart2_4.png](ETL%20and%20ELT%20design%20patterns%20for%20lake%20house%20archite%20a7ad18bd8ea843fc888aa1d3d5246856/ETLandELTRedshiftPart2_4.png)

8. Comment out the following SET statement in the six UNLOAD query files (`ssb-unload<1-3>.sql` and `tickit-unload<1-3>.sql`) to force all six UNLOAD queries to run in the main cluster:  

    ```
    set query_group to 'unload_query';
    ```

    In other words, disable Concurrency Scaling mode for the UNLOAD queries.

9. Run the `concurrency-elt-unload.sh` script. While the script is running, you will see the following sample output:  The following are the response times taken by the script:  

    ![ETL%20and%20ELT%20design%20patterns%20for%20lake%20house%20archite%20a7ad18bd8ea843fc888aa1d3d5246856/ETLandELTRedshiftPart2_5.png](ETL%20and%20ELT%20design%20patterns%20for%20lake%20house%20archite%20a7ad18bd8ea843fc888aa1d3d5246856/ETLandELTRedshiftPart2_5.png)

    ```
    real 3m40.328s user 0m0.104s sys 0m0.000s
    ```

    The following shows the Workload Management settings for the Redshift cluster:

    ![ETL%20and%20ELT%20design%20patterns%20for%20lake%20house%20archite%20a7ad18bd8ea843fc888aa1d3d5246856/ETLandELTRedshiftPart2_6.png](ETL%20and%20ELT%20design%20patterns%20for%20lake%20house%20archite%20a7ad18bd8ea843fc888aa1d3d5246856/ETLandELTRedshiftPart2_6.png)

10. Run the following query to validate that all the queries ran in the main cluster (look for “`which_cluster = Main`” in the query output below):  With Concurrency Scaling, the end-to-end runtime improved by 37.5% (60 seconds faster).       

    ```
    SELECT query, Substring(querytxt,1,90) query_text, starttime starttime_utc, (endtime-starttime)/(1000*1000) elapsed_time_secs, case when aborted= 0 then 'complete' else 'error' end status, case when concurrency_scaling_status = 1 then 'Concurrency Scaling' else 'Main' end which_cluster FROM stl_query WHERE database = 'rselttest' AND starttime between '2019-10-20 23:19:00' and '2019-10-20 23:24:00’ AND userid=100 AND querytxt NOT LIKE 'padb_fetch_sample%' AND (querytxt LIKE 'create%' or querytxt LIKE 'UNLOAD%') ORDER BY query DESC;
    ```

    See the following output from the query:

    ![ETL%20and%20ELT%20design%20patterns%20for%20lake%20house%20archite%20a7ad18bd8ea843fc888aa1d3d5246856/ETLandELTRedshiftPart2_7.png](ETL%20and%20ELT%20design%20patterns%20for%20lake%20house%20archite%20a7ad18bd8ea843fc888aa1d3d5246856/ETLandELTRedshiftPart2_7.png)

    ## Summary

    This post provided a step-by-step walkthrough of a few straightforward examples of the common ELT and ETL design patterns of Amazon Redshift using some key Amazon Redshift features such as [Amazon Redshift Spectrum](https://docs.aws.amazon.com/redshift/latest/dg/c-getting-started-using-spectrum.html), [Concurrency Scaling](https://docs.aws.amazon.com/redshift/latest/dg/concurrency-scaling.html), and recent support for data lake export.

    As always, AWS welcomes feedback. Please submit thoughts or questions in the comments.

    ### About the Authors

    **Asim Kumar Sasmal is a senior data architect – IoT in the Global Specialty Practice of AWS Professional Services.** He helps AWS customers around the globe to design and build data driven solutions by providing expert technical consulting, best practices guidance, and implementation services on AWS platform. He is passionate about working backwards from customer ask, help them to think big, and dive deep to solve real business problems by leveraging the power of AWS platform.

    **Maor Kleider is a principal product manager for Amazon Redshift**, a fast, simple and cost-effective data warehouse. Maor is passionate about collaborating with customers and partners, learning about their unique big data use cases and making their experience even better. In his spare time, Maor enjoys traveling and exploring new restaurants with his family.