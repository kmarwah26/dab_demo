# Databricks notebook source
# MAGIC %md
# MAGIC # Integration Tests for DAB Demo Workflow
# MAGIC 
# MAGIC This notebook tests the deployed workflow end-to-end.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Import Libraries

# COMMAND ----------

from pyspark.sql import SparkSession
from datetime import datetime
import sys

# COMMAND ----------

# MAGIC %md
# MAGIC ## Initialize Test Suite

# COMMAND ----------

print("=" * 60)
print("DAB Demo Integration Tests")
print("=" * 60)
print(f"Test Execution Time: {datetime.now()}")
print("=" * 60)

test_results = []
test_passed = 0
test_failed = 0

def run_test(test_name, test_func):
    """Helper function to run a test and record results"""
    global test_passed, test_failed
    try:
        print(f"\n🧪 Running: {test_name}")
        test_func()
        print(f"✅ PASSED: {test_name}")
        test_results.append((test_name, "PASSED", None))
        test_passed += 1
        return True
    except Exception as e:
        print(f"❌ FAILED: {test_name}")
        print(f"   Error: {str(e)}")
        test_results.append((test_name, "FAILED", str(e)))
        test_failed += 1
        return False

# COMMAND ----------

# MAGIC %md
# MAGIC ## Test 1: Verify Data Preparation Output

# COMMAND ----------

def test_data_preparation_output():
    """Test that Task 1 produced the expected output"""
    spark = SparkSession.builder.getOrCreate()
    
    # Check if the prepared data exists
    input_path = "/tmp/dab_demo/prepared_data"
    df = spark.read.format("delta").load(input_path)
    
    # Verify record count
    record_count = df.count()
    assert record_count > 0, f"Expected records > 0, got {record_count}"
    print(f"   ✓ Found {record_count} records in prepared data")
    
    # Verify schema
    expected_columns = ["id", "name", "age", "department", "processed_at"]
    actual_columns = df.columns
    for col in expected_columns:
        assert col in actual_columns, f"Missing expected column: {col}"
    print(f"   ✓ All expected columns present: {expected_columns}")
    
    # Verify data types
    assert "id" in [f.name for f in df.schema.fields], "Missing id column"
    assert "processed_at" in [f.name for f in df.schema.fields], "Missing processed_at timestamp"
    print(f"   ✓ Schema validation passed")
    
    # Verify no null IDs
    null_ids = df.filter(df.id.isNull()).count()
    assert null_ids == 0, f"Found {null_ids} null IDs"
    print(f"   ✓ No null IDs found")

run_test("Test 1: Data Preparation Output Validation", test_data_preparation_output)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Test 2: Verify Data Quality

# COMMAND ----------

def test_data_quality():
    """Test data quality constraints"""
    spark = SparkSession.builder.getOrCreate()
    
    input_path = "/tmp/dab_demo/prepared_data"
    df = spark.read.format("delta").load(input_path)
    
    # Check for duplicate IDs
    id_count = df.count()
    distinct_id_count = df.select("id").distinct().count()
    assert id_count == distinct_id_count, f"Found duplicate IDs: {id_count} total vs {distinct_id_count} distinct"
    print(f"   ✓ No duplicate IDs ({distinct_id_count} unique IDs)")
    
    # Check age values are reasonable
    from pyspark.sql.functions import min, max
    age_stats = df.select(min("age").alias("min_age"), max("age").alias("max_age")).collect()[0]
    assert age_stats['min_age'] > 0, f"Invalid minimum age: {age_stats['min_age']}"
    assert age_stats['max_age'] < 150, f"Invalid maximum age: {age_stats['max_age']}"
    print(f"   ✓ Age values are valid (range: {age_stats['min_age']}-{age_stats['max_age']})")
    
    # Check department values
    departments = [row.department for row in df.select("department").distinct().collect()]
    assert len(departments) > 0, "No departments found"
    print(f"   ✓ Found {len(departments)} departments: {departments}")

run_test("Test 2: Data Quality Validation", test_data_quality)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Test 3: Verify Analysis Results

# COMMAND ----------

def test_analysis_results():
    """Test that Task 2 produced the expected analysis results"""
    spark = SparkSession.builder.getOrCreate()
    
    # Check department count analysis
    dept_count_path = "/tmp/dab_demo/analysis_results/dept_count"
    dept_df = spark.read.format("delta").load(dept_count_path)
    dept_count = dept_df.count()
    assert dept_count > 0, f"Expected department analysis results, got {dept_count} records"
    print(f"   ✓ Department count analysis completed ({dept_count} departments)")
    
    # Verify columns in department count
    assert "department" in dept_df.columns, "Missing department column in analysis"
    assert "employee_count" in dept_df.columns, "Missing employee_count column in analysis"
    print(f"   ✓ Department count has correct schema")
    
    # Check age statistics analysis
    age_stats_path = "/tmp/dab_demo/analysis_results/age_stats"
    age_df = spark.read.format("delta").load(age_stats_path)
    age_stats_count = age_df.count()
    assert age_stats_count > 0, f"Expected age statistics results, got {age_stats_count} records"
    print(f"   ✓ Age statistics analysis completed ({age_stats_count} departments)")
    
    # Verify columns in age statistics
    expected_cols = ["department", "count", "avg_age", "min_age", "max_age"]
    for col in expected_cols:
        assert col in age_df.columns, f"Missing column in age stats: {col}"
    print(f"   ✓ Age statistics has correct schema")

run_test("Test 3: Analysis Results Validation", test_analysis_results)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Test 4: Verify Data Consistency

# COMMAND ----------

def test_data_consistency():
    """Test consistency between preparation and analysis outputs"""
    spark = SparkSession.builder.getOrCreate()
    
    # Load prepared data
    prepared_path = "/tmp/dab_demo/prepared_data"
    prepared_df = spark.read.format("delta").load(prepared_path)
    prepared_count = prepared_df.count()
    
    # Load analysis results
    dept_count_path = "/tmp/dab_demo/analysis_results/dept_count"
    dept_df = spark.read.format("delta").load(dept_count_path)
    
    # Sum of department counts should equal total records
    from pyspark.sql.functions import sum
    total_from_analysis = dept_df.select(sum("employee_count")).collect()[0][0]
    
    assert prepared_count == total_from_analysis, \
        f"Inconsistent counts: prepared={prepared_count}, analysis={total_from_analysis}"
    print(f"   ✓ Data consistency verified ({prepared_count} records)")

run_test("Test 4: Data Consistency Validation", test_data_consistency)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Test Summary and Results

# COMMAND ----------

print("\n" + "=" * 60)
print("TEST EXECUTION SUMMARY")
print("=" * 60)

for test_name, status, error in test_results:
    status_icon = "✅" if status == "PASSED" else "❌"
    print(f"{status_icon} {test_name}: {status}")
    if error:
        print(f"   Error: {error}")

print("\n" + "-" * 60)
print(f"Total Tests: {len(test_results)}")
print(f"Passed: {test_passed} ✅")
print(f"Failed: {test_failed} ❌")
print(f"Success Rate: {(test_passed/len(test_results)*100):.1f}%")
print("=" * 60)

# Exit with appropriate code
if test_failed > 0:
    print("\n❌ TESTING FAILED - Some tests did not pass")
    dbutils.notebook.exit("FAILED")
else:
    print("\n✅ ALL TESTS PASSED")
    dbutils.notebook.exit("SUCCESS")

# COMMAND ----------




