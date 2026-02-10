# Databricks notebook source
# MAGIC %md
# MAGIC # Task 1: Data Preparation
# MAGIC 
# MAGIC This notebook performs initial data preparation steps.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Import Libraries

# COMMAND ----------

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, current_timestamp, lit
from datetime import datetime

# COMMAND ----------

# MAGIC %md
# MAGIC ## Initialize Spark Session

# COMMAND ----------

spark = SparkSession.builder.appName("Task1-DataPreparation").getOrCreate()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Generate Sample Data

# COMMAND ----------

print("=" * 50)
print("Task 1: Data Preparation Started")
print("=" * 50)
print(f"Timestamp: {datetime.now()}")

# Create sample data
data = [
    (1, "Alice", 25, "Engineering"),
    (2, "Bob", 30, "Marketing"),
    (3, "Charlie", 35, "Sales"),
    (4, "Diana", 28, "Engineering"),
    (5, "Eve", 32, "Marketing"),
    (6, "Frank", 29, "Sales"),
    (7, "Grace", 31, "Engineering"),
    (8, "Henry", 27, "Marketing"),
    (9, "Ivy", 33, "Sales"),
    (10, "Jack", 26, "Engineering")
]

columns = ["id", "name", "age", "department"]

df = spark.createDataFrame(data, columns)

# Add processing timestamp
df = df.withColumn("processed_at", current_timestamp())

print(f"\nGenerated {df.count()} records")
print("\nSample Data:")
df.show(10, truncate=False)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Save Prepared Data

# COMMAND ----------

# Save to a temporary table for the next task
temp_table = "prepared_data"
df.createOrReplaceTempView(temp_table)

# Optionally save to Delta table
output_path = "/tmp/dab_demo/prepared_data"
df.write.format("delta").mode("overwrite").save(output_path)

print(f"\nData saved to: {output_path}")
print(f"Temporary view created: {temp_table}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Task Summary

# COMMAND ----------

print("=" * 50)
print("Task 1: Data Preparation Completed Successfully")
print("=" * 50)
print(f"Total records processed: {df.count()}")
print(f"Columns: {', '.join(df.columns)}")
print(f"Output location: {output_path}")

