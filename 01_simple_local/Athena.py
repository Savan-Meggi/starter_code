import logging
import os
from pyathena import connect
from pyathena.pandas.cursor import PandasCursor

# ------------------- Setup -------------------
aws_profile = "data-science"
s3_staging_dir = "s3://det-testing-bucket/athena_results/"
athena_table_name = 's3_history_data.telit_parsed_measurements'

# ------------------- Logging -------------------
log_file = os.path.join(os.path.dirname(__file__), "Athena_pipeline.log")
logging.basicConfig(filename=log_file, level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger()

# ------------------- Connect to Athena -------------------
print("Connecting to Athena...")

try:
    cursor = connect(
        profile_name=aws_profile,
        s3_staging_dir=s3_staging_dir,
        cursor_class=PandasCursor
    ).cursor()

    print("Connected to Athena successfully")

except Exception as e:
    print(f"Failed to connect to Athena: {e}")
    raise SystemExit(1)

# ------------------- Run query -------------------
athena_query = f"""
SELECT *
FROM {athena_table_name}
LIMIT 10
"""

try:
    df = cursor.execute(athena_query).as_pandas()

    print(f"Query returned {len(df)} rows")
    print(df)

except Exception as e:
    print(f"Athena query failed: {e}")
    raise SystemExit(1)

# ------------------- Close -------------------
cursor.close()

print("Athena connection closed")
