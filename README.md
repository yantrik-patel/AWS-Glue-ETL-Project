# AWS-Glue-ETL-Project
This repo is for demonstration of ETL pipeline that runs on AWS Glue.


Following is the Flowchart of whole pipeline that I have built

![image](https://github.com/yantrik-patel/AWS-Glue-ETL-Project/assets/116425101/18a890dc-f523-4db1-99d7-ba9f94f13d97)

<details>

<summary>IAM Roles and Policies</summary>

(1) glue_crawler_role: This is glue role for S3 Bucket access, Cloudwatch Logs and Glue permissions.   
    Following policies needs to be attached to this role   
    - AmazonS3FullAccess  
    - AWSGlueServiceRole   
    - CloudWatchFullAccess   
    
(2) glue_redshift_role: This is glue role for Redshift access, S3 access and Glue permissions.   
    Following policies needs to be attached to this role   
    - AmazonRedshiftFullAccess  
    - AmazonS3FullAccess   
    - AWSGlueServiceRole



</details>


<details>

<summary>Source File S3 Buckets</summary>

Bucket name is 'glue-etl-project-yantrik'

I have created a folder named 'input' where our client will upload the files.

Few more folders are created
- output---> to store the processed files(parquet files)
- scripts---> to store the glue scripts
- temp---> to store the glue/spark intermediate actions and results

![image](https://github.com/yantrik-patel/AWS-Glue-ETL-Project/assets/116425101/ddca23e3-ff1e-4fa9-8e4a-7a6bb07ca7d8)



</details>


<details>

<summary>Creating the 1st Glue Job</summary>


<details>

<summary>Creating the Glue Database</summary>
Let's create the database 'mydatabase'


![image](https://github.com/yantrik-patel/AWS-Glue-ETL-Project/assets/116425101/18974c10-a2d2-44e0-b81c-4d54c954488e)

</details>

<details>

<summary>Creating the 1st Glue Crawler</summary>

![image](https://github.com/yantrik-patel/AWS-Glue-ETL-Project/assets/116425101/62272fdd-d5cf-4f51-aa69-3b0a6a9a8f4c)

Following are the further details we need to provide for creating the crawler

- Crawler Details:
    - Name: 'crawl_source_s3_files'
- Data source configuration:
    - Add data source: choose S3 bucker folder upto 'product' folder. So glue will create a table named 'product'.
- Configure security settings
    - IAM Role: choose from the roles we created earlier
- Set output and scheduling
    - Output configuration: Target database: choose 'mydatabase'
    - Crawler schedule: On Demand
 
Now the crawler is created, we can run the crawler. This will create product table in mydatabase DB and we can query the data from ATHENA.
</details>




<details>
<summary>Creating 1st Glue Job</summary>

![image](https://github.com/yantrik-patel/AWS-Glue-ETL-Project/assets/116425101/83732fea-dfb9-45f5-9377-074d372cf323)

- **source**: The product table in mydatabase that glue crawler have created
- **transformation**: Change Schema---We will do below mentioned steps with in the script itself.
  The transformation script is available in this repo. File name is 'glue_job_read_from_source_s3.py'.
  following are the transformation steps:
  
      - column name changed in Glue Dynamic Frame.
      - column 'seller_id' have few alphabetic values which is not correct, so those are filtered out with ResolveChoice method(by type casting to long datatype).
      - converted Glue Dynamic Frame to Spark Dataframe.
      - Filtered not null seller_id and added new column with value 'Active'
      - converted Spark Dataframe into temp view and done aggregating using SQL command.
      - converted Spark Dataframe back into Glue Dynamic Dataframe.
      - write the parquet file into target S3 bucket folder.
  
- **target**: the target will be our S3 bucket's output folder
  
![image](https://github.com/yantrik-patel/AWS-Glue-ETL-Project/assets/116425101/a0282445-e20c-44ca-bb02-d94515b01f37)

Once the job runs successfully, we will have parquet file in S3 output folder.
</details>

</details>
<details>
<summary>Creating Redshift Cluster</summary>   
Following are the steps to create Redshift cluster   

- Search 'Redshift' in navigation bar.
- Click 'create cluster'
- Choose 'node type' dc2.large as I have free tier account and data volume is very less.
- AZ configuration: single AZ is good enough for our poc
- Associated IAM roles: create the default role and associate it.
- click on the 'create cluster'
    
</details>

<details>
<summary>Creating 2nd Glue Job</summary>
<details>
<summary>Creating Glue Connection with Redshift DB</summary>
We need to create a Glue connection with Redshift DB so that Glue can read table and decide schema.   
Go to 'connection' on Glue console screen   

![image](https://github.com/yantrik-patel/AWS-Glue-ETL-Project/assets/116425101/2594d3e9-45d2-4eb7-ac87-a6a2151f2a31)

- click 'create connection'
- choose 'redshift' as data source
- select redshift cluster that was created earlier
- select database name(create a new database in redshift if you don't have)
- select username and provide password for connector to access redshift cluster
- click 'create connection'

Once the connection is created you can test the connection, following are the steps.
- choose from connection tab
- from Action drop down, click 'test connection'
- first it will give error as Redshift cluster is running in seperate subnet which can't find the s3 so we need to create S3 endpoint. Go to VPC screen from navigation search bar. Click on the 'endpoints' and create an endpoint, in 'services' search box, search for S3 and select option with type as 'Gateway' and click on create Endpoint.
Now again test the connection and error should go away.

</details>
<details>
<summary>Creating a crawler</summary>
We need to create one more crawler named 'crawl-redshift-table' which will crawl through table and prepare schema.
The steps are same as 1st crawler creating except the data source will be JDBC. And connection should be the one we created in previous step



![image](https://github.com/yantrik-patel/AWS-Glue-ETL-Project/assets/116425101/0113a1a9-64eb-46e4-b138-49250a515b9d)

</details>

<details>
<summary>Creating the 2nd Glue Job</summary>
Like the 1st glue job, we need to select 'visual etl'   
Following sould be the source, transformation and target configurations
    
- **source:** S3 Bucket's output folder where parquet files are stored    
- **transformation:** simply select the 'change schema'(I have done column renaming based on Redshift table column names in scripts itself)
- **target:** redshift table that we created.

once this are configured, give the job name and other basic details and move on to scripts tab and click on 'edit script'.   
in the script, column names are mapped with the target(Redshift) table column names. The script code can be found in this repo file name is 'glue_job_insert_into_redshift.py'   

We can now run the job and at the end Redshift table will be populated.   

![image](https://github.com/yantrik-patel/AWS-Glue-ETL-Project/assets/116425101/9fb9135d-637d-4dca-92d0-415f9f9d10ae)

</details>    
</details>
<details>
<summary>Orchestration</summary>
    I have used Glue Workflow to orchastrate the whole process. Following is the flow   

        
- 1st trigger is on demand, which starts running 1st Glue crawler.
- After 1st Glue crawler runs successfully, 1st Glue Job starts running.
- After successfull run of 1st Glue Job, 2nd crawler is triggered.
- After 2nd crawler run is success, 2nd Glue job starts running.


![image](https://github.com/yantrik-patel/AWS-Glue-ETL-Project/assets/116425101/31861410-ded8-46f0-9919-844073fe6cec)

    
</details>







