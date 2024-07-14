import json
import kafka
from pyspark.sql import SparkSession
from pyspark.sql.functions import *

# Initialize Spark Session
spark = SparkSession.builder.appName("UserBehaviorPipeline").getOrCreate()

# Kafka configuration
kafka_brokers = "localhost:9092"
kafka_topic = "user_behavior"

# Read data from Kafka
df = spark.readStream.format("kafka").option("kafka.bootstrap.servers", kafka_brokers).option("subscribe", kafka_topic).load()

# Data processing
df = df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")
df = df.withColumn("jsonData", from_json(col("value"), schema))
df = df.select("jsonData.*")

# Write processed data to storage
query = df.writeStream.format("parquet").option("checkpointLocation", "/path/to/checkpoint/dir").option("path", "/path/to/output/dir").start()

query.awaitTermination()
