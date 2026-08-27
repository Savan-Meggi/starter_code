import logging
import os
from datetime import datetime, timezone
from pyathena import connect
from pyathena.pandas.cursor import PandasCursor

# ------------------- Environment setup -------------------
is_local = True  # Set to False for AWS/CloudFormation
aws_profile = "data-science"  # AWS profile used when running locally
s3_staging_dir = "s3://det-testing-bucket/athena_results/"  # S3 location for Athena query results
athena_table_name = 's3_history_data.telit_parsed_measurements' # S3 data

# ------------------- Logging -------------------
log_file = os.path.join(os.path.dirname(__file__), "Athena_pipeline.log")
logging.basicConfig(filename=log_file, level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger()

# ------------------- Pipeline start -------------------
pipeline_start_time = datetime.now(timezone.utc)
logger.info(f"Pipeline start: {pipeline_start_time}")
print(f"Pipeline start: {pipeline_start_time}")

# ------------------- Connect to Athena -------------------
logger.info("Connecting to AWS Athena")
print("Connecting to AWS Athena")

try:
    if is_local:
        cursor = connect(
            profile_name=aws_profile,
            s3_staging_dir=s3_staging_dir,
            cursor_class=PandasCursor
        ).cursor()  # Local development
        print(f"Using AWS profile: {aws_profile}")
    else:
        cursor = connect(
            s3_staging_dir=s3_staging_dir,
            cursor_class=PandasCursor
        ).cursor()  # AWS CloudFormation
        print("Using AWS CloudFormation role")

    logger.info("Connected to Athena successfully")
    print("Connected to Athena successfully")

except Exception as e:
    logger.error(f"Failed to connect to Athena: {e}")
    print(f"ERROR: Failed to connect to Athena: {e}")
    raise SystemExit(1)

# ------------------- Athena connection ready -------------------
print("Athena connection is ready.")

# ------------------- Example Athena query -------------------
# athena_query = f"""
# SELECT *
# FROM {athena_table_name}
# LIMIT 10
# """
# df = cursor.execute(athena_query).as_pandas()
# print(df)

# ------------------- Close Athena connection -------------------
cursor.close()
logger.info("Athena connection closed")
print("Athena connection closed")

# ------------------- Pipeline complete -------------------
pipeline_end_time = datetime.now(timezone.utc)
logger.info(f"Pipeline finished: {pipeline_end_time}")
print(f"Pipeline finished: {pipeline_end_time}")
