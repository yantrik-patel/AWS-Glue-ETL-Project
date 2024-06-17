import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue import DynamicFrame

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Script generated for node Amazon S3
AmazonS3_node1718626669294 = glueContext.create_dynamic_frame.from_options(format_options={}, connection_type="s3", format="parquet", connection_options={"paths": ["s3://glue-etl-project-yantrik/output/"], "recurse": True}, transformation_ctx="AmazonS3_node1718626669294")

# Script generated for node Change Schema
ChangeSchema_node1718626671319 = ApplyMapping.apply(frame=AmazonS3_node1718626669294, mappings=[("new_year", "string", "year", "string"), ("cnt", "long", "noofcustomers", "BIGINT"), ("qty", "long", "quantity", "BIGINT")], transformation_ctx="ChangeSchema_node1718626671319")

# Script generated for node Amazon Redshift
AmazonRedshift_node1718626673835 = glueContext.write_dynamic_frame.from_options(frame=ChangeSchema_node1718626671319, connection_type="redshift", connection_options={"redshiftTmpDir": "s3://glue-etl-project-yantrik/temp/", "useConnectionProperties": "true", "dbtable": "public.product_table_def", "connectionName": "Redshift connection", "preactions": "CREATE TABLE IF NOT EXISTS public.product_table_def (new_year VARCHAR, cnt BIGINT, qty BIGINT);"}, transformation_ctx="AmazonRedshift_node1718626673835")



job.commit()