import boto3
import json
import logging
import os
import pymysql

# ------------------- Setup -------------------
aws_profile = "data-science"
aws_region = "eu-west-1"

# ------------------- Logging -------------------
log_file = os.path.join(os.path.dirname(__file__), "RDS_pipeline.log")
logging.basicConfig(filename=log_file, level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger()

# ------------------- Connect to AWS -------------------
print("Connecting to AWS...")

try:
    session = boto3.Session(profile_name=aws_profile, region_name=aws_region)

    print("Connected to AWS successfully")

except Exception as e:
    print(f"Failed to connect to AWS: {e}")
    raise SystemExit(1)

# ------------------- Get RDS credentials -------------------
try:
    secrets_client = session.client("secretsmanager", region_name=aws_region)
    secret = json.loads(secrets_client.get_secret_value(SecretId="device_data_rds")["SecretString"])

    print("RDS credentials retrieved successfully")

except Exception as e:
    print(f"Failed to get RDS credentials: {e}")
    raise SystemExit(1)

# ------------------- Connect to RDS -------------------
try:
    conn = pymysql.connect(
        host=secret["host"],
        user=secret["username"],
        password=secret["password"],
        port=int(secret["port"]),
        database="parsed"
    )

    print("Connected to RDS successfully")

except Exception as e:
    print(f"Failed to connect to RDS: {e}")
    raise SystemExit(1)

# ------------------- Run query -------------------
try:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM scratch_sm.pipeline_metrics1 LIMIT 10")
    results = cursor.fetchall()

    print(f"Query returned {len(results)} rows")

    for row in results:
        print(row)

except Exception as e:
    print(f"RDS query failed: {e}")
    raise SystemExit(1)

# ------------------- Close -------------------
cursor.close()
conn.close()

print("RDS connection closed")
