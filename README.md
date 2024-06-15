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
- **transformation**: Change Schema---We will rename column, fix the datatype, do aggregation and write the final file in Parquet format later with in the script itself.
  The transformation script is available in this repo. File name is 'glue_job_read_from_source_s3.py'.
  
- **target**: the target will be our S3 bucket's output folder
  
![image](https://github.com/yantrik-patel/AWS-Glue-ETL-Project/assets/116425101/a0282445-e20c-44ca-bb02-d94515b01f37)

Once the job runs successfully, we will have parquet file in S3 output folder.
</details>

</details>

