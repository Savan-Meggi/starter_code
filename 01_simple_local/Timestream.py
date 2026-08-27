import boto3
import logging
import os
from datetime import datetime, timezone

# ------------------- Setup -------------------
aws_profile = "prod-timestream"
aws_region = "eu-west-1"

# ------------------- Logging -------------------
log_file = os.path.join(os.path.dirname(__file__), "Timestream_pipeline.log")
logging.basicConfig(filename=log_file, level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger()

# ------------------- Connect to Timestream -------------------
print("Connecting to Timestream...")

try:
    session = boto3.Session(profile_name=aws_profile, region_name=aws_region)
    ts_client = session.client("timestream-query", region_name=aws_region)

    print("Connected to Timestream successfully")

except Exception as e:
    print(f"Failed to connect to Timestream: {e}")
    raise SystemExit(1)

# ------------------- Run query -------------------
timestream_query = """
SELECT *
FROM DeviceData.RawData
LIMIT 10
"""

try:
    response = ts_client.query(QueryString=timestream_query)

    print("Timestream query completed successfully")
    print(f"Query returned {len(response['Rows'])} rows")
    print(response)

except Exception as e:
    print(f"Timestream query failed: {e}")
    raise SystemExit(1)

# ------------------- Close -------------------
print("Timestream connection complete")
