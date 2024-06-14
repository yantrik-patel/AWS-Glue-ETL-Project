# AWS-Glue-ETL-Project
This repo is for demonstration of ETL pipeline that runs on AWS Glue.

<details>

<summary>IAM Roles and Policies</summary>

First of all, we need to create an IAM Role(my role name is 'glue_crawler_role') on which we will attach few policies so that AWS Glue can access S3 Bucket, Cloudwatch Logs and Glue permissions.

Following are the policies we need to attach with the role 'glue_crawler_role'


![image](https://github.com/yantrik-patel/AWS-Glue-ETL-Project/assets/116425101/928e72a1-812e-490c-ac90-0a0570b04145)



</details>


<details>

<summary>Source File S3 Buckets</summary>

Bucket name is 'glue-etl-project-yantrik'

I have created a folder named 'input' where our client will upload the files.

Few more folders are created
- output---> to store the processed files
- scripts---> to store the glue scripts
- temp---> to store the glue/spark intermediate actions and results

![image](https://github.com/yantrik-patel/AWS-Glue-ETL-Project/assets/116425101/ddca23e3-ff1e-4fa9-8e4a-7a6bb07ca7d8)



</details>
