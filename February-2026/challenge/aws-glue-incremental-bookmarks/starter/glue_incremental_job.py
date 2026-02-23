"""
Minimal starter for AWS Glue incremental ETL with job bookmarks.
Participants should implement read options, transformations, and write strategy.
"""

import sys
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext

# Extend based on your design.
args = getResolvedOptions(sys.argv, ["JOB_NAME", "SOURCE_PATH", "TARGET_PATH"])

sc = SparkContext()
glue_context = GlueContext(sc)
spark = glue_context.spark_session
job = Job(glue_context)
job.init(args["JOB_NAME"], args)

# STEP 1: Read from SOURCE_PATH using a bookmark-tracked transformation_ctx.
# STEP 2: Apply your required transformations.
# STEP 3: Write curated output to TARGET_PATH.
# STEP 4: Commit job.

job.commit()
