# Databricks notebook source
# MAGIC %md
# MAGIC # Task 2: Data Analysis
# MAGIC 
# MAGIC This notebook analyzes the data prepared in Task 1.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Import Libraries

# COMMAND ----------

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, avg, max, min
from datetime import datetime

# COMMAND ----------

# MAGIC %md
# MAGIC ## Initialize Spark Session

# COMMAND ----------

spark = SparkSession.builder.appName("Task2-DataAnalysis").getOrCreate()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Load Prepared Data

# COMMAND ----------

print("=" * 50)
print("Task 2: Data Analysis Started")
print("=" * 50)
print(f"Timestamp: {datetime.now()}")

# Read from Delta table created in Task 1
input_path = "/tmp/dab_demo/prepared_data"
df = spark.read.format("delta").load(input_path)

print(f"\nLoaded {df.count()} records from: {input_path}")
print("\nData Schema:")
df.printSchema()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Perform Analysis

# COMMAND ----------

# Analysis 1: Count by Department
print("\n" + "=" * 50)
print("Analysis 1: Employee Count by Department")
print("=" * 50)

dept_count = df.groupBy("department").agg(
    count("*").alias("employee_count")
).orderBy("employee_count", ascending=False)

dept_count.show(truncate=False)

# COMMAND ----------

# Analysis 2: Age Statistics by Department
print("\n" + "=" * 50)
print("Analysis 2: Age Statistics by Department")
print("=" * 50)

age_stats = df.groupBy("department").agg(
    count("*").alias("count"),
    avg("age").alias("avg_age"),
    min("age").alias("min_age"),
    max("age").alias("max_age")
).orderBy("department")

age_stats.show(truncate=False)

# COMMAND ----------

# Analysis 3: Overall Statistics
print("\n" + "=" * 50)
print("Analysis 3: Overall Statistics")
print("=" * 50)

overall_stats = df.agg(
    count("*").alias("total_employees"),
    avg("age").alias("average_age"),
    min("age").alias("youngest"),
    max("age").alias("oldest")
).collect()[0]

print(f"Total Employees: {overall_stats['total_employees']}")
print(f"Average Age: {overall_stats['average_age']:.2f}")
print(f"Youngest Employee: {overall_stats['youngest']}")
print(f"Oldest Employee: {overall_stats['oldest']}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Save Analysis Results

# COMMAND ----------

# Save department summary
output_path = "/tmp/dab_demo/analysis_results"

dept_count.write.format("delta").mode("overwrite").save(f"{output_path}/dept_count")
age_stats.write.format("delta").mode("overwrite").save(f"{output_path}/age_stats")

print(f"\nAnalysis results saved to: {output_path}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Task Summary

# COMMAND ----------

print("=" * 50)
print("Task 2: Data Analysis Completed Successfully")
print("=" * 50)
print(f"Records analyzed: {df.count()}")
print(f"Departments analyzed: {df.select('department').distinct().count()}")
print(f"Output location: {output_path}")

