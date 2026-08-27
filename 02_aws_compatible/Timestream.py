import boto3
import logging
import os
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

# ------------------- Environment setup -------------------
is_local = True  # Set to False for AWS/CloudFormation
aws_profile = "prod-timestream"  # AWS profile used when running locally
aws_region = "eu-west-1"  # AWS region
timestream_role = "arn:aws:iam::507038060985:role/DataScience-Timestream-ReadOnlyRole"  # AWS CloudFormation role

# ------------------- Logging -------------------
log_file = os.path.join(os.path.dirname(__file__), "Timestream_pipeline.log")
logging.basicConfig(filename=log_file, level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger()

# ------------------- Pipeline start -------------------
pipeline_start_time = datetime.now(timezone.utc)
logger.info(f"Pipeline start: {pipeline_start_time}")
print(f"Pipeline start: {pipeline_start_time}")

# ------------------- Assume Timestream role ------------------- <----------- For AWS CloudFormation
def assume_timestream_role(role_arn):
    sts_client = boto3.client("sts", region_name=aws_region)
    assumed = sts_client.assume_role(RoleArn=role_arn, RoleSessionName="TimestreamSession")
    creds = assumed["Credentials"]

    return boto3.Session(
        aws_access_key_id=creds["AccessKeyId"],
        aws_secret_access_key=creds["SecretAccessKey"],
        aws_session_token=creds["SessionToken"],
        region_name=aws_region
    )

# ------------------- Run Timestream query -------------------
def run_timestream_query(query, client):
    response = client.query(QueryString=query)
    return response

# ------------------- Connect to Timestream -------------------
start_time_timestream = datetime.now(ZoneInfo("Europe/London"))

logger.info("Connecting to AWS Timestream")
print("Connecting to AWS Timestream")

try:
    if is_local:
        session = boto3.Session(profile_name=aws_profile, region_name=aws_region)  # Local development
        print(f"Using AWS profile: {aws_profile}")
    else:
        session = assume_timestream_role(timestream_role)  # AWS CloudFormation
        print("Using AWS CloudFormation role")

    # Create the Timestream query client
    ts_client = session.client("timestream-query", region_name=aws_region)

    logger.info("Connected to Timestream successfully")
    print("Connected to Timestream successfully")

except Exception as e:
    logger.error(f"Failed to connect to Timestream: {e}")
    print(f"ERROR: Failed to connect to Timestream: {e}")
    raise SystemExit(1)

# ------------------- Timestream query -------------------
# timestream_query = """
# SELECT DISTINCT *
# FROM DeviceData.RawData
# LIMIT 10
# """
# 
# start_query = datetime.now(ZoneInfo("Europe/London"))
# logger.info(f"Timestream timestream_query start: {start_query}")
# print(f"Timestream timestream_query start: {start_query}")
# 
# try:
#     timestream_raw = run_timestream_query(timestream_query, ts_client)
#     logger.info("Timestream query completed successfully")
#     print("Timestream query completed successfully")
# 
# except Exception as e:
#     logger.error(f"Timestream query failed: {e}")
#     print(f"ERROR: Timestream query failed: {e}")
#     raise SystemExit(1)
# 
# # ------------------- Query results -------------------
# print("Query returned successfully")
# print(timestream_raw)

# ------------------- Pipeline complete -------------------
pipeline_end_time = datetime.now(timezone.utc)
logger.info(f"Pipeline finished: {pipeline_end_time}")
print(f"Pipeline finished: {pipeline_end_time}")
