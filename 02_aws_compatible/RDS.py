import boto3
import json
import logging
import os
import pymysql
from datetime import datetime, timezone

# ------------------- Environment setup -------------------
is_local = True  # Set to False for AWS/CloudFormation
aws_profile = "data-science"  # AWS profile used when running locally
aws_region = "eu-west-1"  # AWS region

# ------------------- Logging -------------------
log_file = os.path.join(os.path.dirname(__file__), "RDS_pipeline.log")
logging.basicConfig(filename=log_file, level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger()

# ------------------- Pipeline start -------------------
pipeline_start_time = datetime.now(timezone.utc)
logger.info(f"Pipeline start: {pipeline_start_time}")
print(f"Pipeline start: {pipeline_start_time}")

# ------------------- Connect to AWS ------------------- <----------- For AWS CloudFormation
logger.info("Connecting to AWS")
print("Connecting to AWS")

try:
    if is_local:
        session = boto3.Session(profile_name=aws_profile, region_name=aws_region)  # Local development
        print(f"Using AWS profile: {aws_profile}")
    else:
        session = boto3.Session(region_name=aws_region)  # AWS CloudFormation
        print("Using AWS CloudFormation role")

    logger.info("Connected to AWS successfully")
    print("Connected to AWS successfully")

except Exception as e:
    logger.error(f"Failed to connect to AWS: {e}")
    print(f"ERROR: Failed to connect to AWS: {e}")
    raise SystemExit(1)

# ------------------- Get RDS credentials -------------------
logger.info("Getting RDS credentials from Secrets Manager")
print("Getting RDS credentials from Secrets Manager")

try:
    secrets_client = session.client("secretsmanager", region_name=aws_region)
    secret = json.loads(secrets_client.get_secret_value(SecretId="device_data_rds")["SecretString"])

    logger.info("RDS credentials retrieved successfully")
    print("RDS credentials retrieved successfully")

except Exception as e:
    logger.error(f"Failed to get RDS credentials: {e}")
    print(f"ERROR: Failed to get RDS credentials: {e}")
    raise SystemExit(1)

# ------------------- Connect to RDS -------------------
logger.info("Connecting to RDS")
print("Connecting to RDS")

try:
    conn = pymysql.connect(
        host=secret["host"],
        user=secret["username"],
        password=secret["password"],
        port=int(secret["port"]),
        database="parsed"
    )

    logger.info("Connected to RDS successfully")
    print("Connected to RDS successfully")

except Exception as e:
    logger.error(f"Failed to connect to RDS: {e}")
    print(f"ERROR: Failed to connect to RDS: {e}")
    raise SystemExit(1)

# ------------------- RDS connection ready -------------------
print("RDS connection is ready.")

# ------------------- Example RDS query -------------------
# Add your SQL query here.
#
# cursor = conn.cursor()
# cursor.execute("SELECT * FROM scratch_sm.pipeline_metrics1 LIMIT 10")
# results = cursor.fetchall()
# for row in results:
#     print(row)

# ------------------- Close RDS connection -------------------
conn.close()
logger.info("RDS connection closed")
print("RDS connection closed")

# ------------------- Pipeline complete -------------------
pipeline_end_time = datetime.now(timezone.utc)
logger.info(f"Pipeline finished: {pipeline_end_time}")
print(f"Pipeline finished: {pipeline_end_time}")
