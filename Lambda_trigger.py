import json
import os
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


#import boto3 for AWS Glue
import boto3
client = boto3.client('glue')

#variable for the job:
glueJobName="TestJobDemo"


#define lambda function

def lambda_handler(event, context):
	logger.info("triggered by event:")
	logger.info(event['detail'])
	response = client.start_job_run(JobName= glueJobName)
	logger.info('started glue job:'+ glueJobName)
	logger.info('Glue job run id' + response['JobRunId'])
	return response