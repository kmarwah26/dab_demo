# Integration Testing Guide

## Overview

This document describes the integrated testing framework for the DAB Demo project. The testing framework validates the entire workflow pipeline end-to-end, ensuring data quality and pipeline correctness.

## Architecture

### Test Components

1. **Test Notebook** (`tests/test_workflow.py`)
   - Main test suite that validates the workflow
   - Runs as a Databricks job
   - Produces detailed test reports

2. **Test Workflow** (`resources/test_workflow.yml`)
   - Databricks job definition for running tests
   - Configured with single-node cluster for cost efficiency
   - Shorter timeout (2 minutes) for quick feedback

3. **Test Execution Script** (`run_tests.sh`)
   - Bash script for end-to-end testing
   - Orchestrates deployment, workflow execution, and testing
   - Provides clear output and error handling

4. **Post-Deployment Hooks** (in `databricks.yml`)
   - Automatic test execution after deployment
   - Configured per environment (dev/prod)

## Test Suite Details

### Test 1: Data Preparation Output Validation

**Purpose**: Verify that Task 1 (Data Preparation) produces expected output.

**Checks**:
- ✅ Delta table exists at expected path
- ✅ Record count is greater than zero
- ✅ All expected columns are present (id, name, age, department, processed_at)
- ✅ Schema types are correct
- ✅ No null values in ID column

**Failure Scenarios**:
- Task 1 failed to run
- Output path is incorrect
- Data is malformed

### Test 2: Data Quality Validation

**Purpose**: Ensure data quality standards are met.

**Checks**:
- ✅ No duplicate IDs
- ✅ Age values are within valid range (0-150)
- ✅ Department values exist
- ✅ All required fields are populated

**Failure Scenarios**:
- Data contains duplicates
- Invalid data values (negative ages, etc.)
- Missing required fields

### Test 3: Analysis Results Validation

**Purpose**: Verify that Task 2 (Data Analysis) produces correct outputs.

**Checks**:
- ✅ Department count analysis exists
- ✅ Age statistics analysis exists
- ✅ Output schemas are correct
- ✅ All expected aggregations are present

**Failure Scenarios**:
- Task 2 failed to run
- Analysis outputs are missing
- Incorrect schema in results

### Test 4: Data Consistency Validation

**Purpose**: Ensure consistency between pipeline stages.

**Checks**:
- ✅ Sum of department counts equals total prepared records
- ✅ No data loss between stages
- ✅ Referential integrity maintained

**Failure Scenarios**:
- Data loss between stages
- Incorrect aggregations
- Inconsistent counts

## Running Tests

### Method 1: Automatic Post-Deployment Testing

The simplest way to run tests is to deploy the bundle. Tests will run automatically:

```bash
databricks bundle deploy --target dev
```

**Process**:
1. Bundle is validated
2. Resources are deployed to Databricks
3. Main workflow is executed
4. Integration tests are run
5. Results are reported

### Method 2: Using the Test Script

For more control and visibility, use the test script:

```bash
# Make script executable (first time only)
chmod +x run_tests.sh

# Run tests for dev environment
./run_tests.sh dev

# Run tests for prod environment
./run_tests.sh prod
```

**Script Steps**:
1. Validates Databricks CLI is installed
2. Deploys bundle to specified environment
3. Runs main workflow
4. Waits for data persistence
5. Runs integration tests
6. Reports success/failure

### Method 3: Manual Testing

Run components individually for debugging:

```bash
# 1. Deploy the bundle
databricks bundle deploy --target dev

# 2. Run the main workflow
databricks bundle run demo_workflow --target dev

# 3. Wait for completion (check in UI or use CLI)
# databricks jobs list-runs --job-id <job-id>

# 4. Run integration tests
databricks bundle run integration_tests --target dev
```

### Method 4: CI/CD Pipeline

For automated testing in CI/CD, see `.github-workflows-example.yml` for a GitHub Actions example.

## Interpreting Test Results

### Success Output

When all tests pass, you'll see:

```
==========================================================
TEST EXECUTION SUMMARY
==========================================================
✅ Test 1: Data Preparation Output Validation: PASSED
✅ Test 2: Data Quality Validation: PASSED
✅ Test 3: Analysis Results Validation: PASSED
✅ Test 4: Data Consistency Validation: PASSED

----------------------------------------------------------
Total Tests: 4
Passed: 4 ✅
Failed: 0 ❌
Success Rate: 100.0%
==========================================================
✅ ALL TESTS PASSED
```

### Failure Output

When tests fail, you'll see detailed error information:

```
==========================================================
TEST EXECUTION SUMMARY
==========================================================
✅ Test 1: Data Preparation Output Validation: PASSED
❌ Test 2: Data Quality Validation: FAILED
   Error: Found duplicate IDs: 10 total vs 8 distinct
✅ Test 3: Analysis Results Validation: PASSED
❌ Test 4: Data Consistency Validation: FAILED
   Error: Inconsistent counts: prepared=10, analysis=8

----------------------------------------------------------
Total Tests: 4
Passed: 2 ✅
Failed: 2 ❌
Success Rate: 50.0%
==========================================================
❌ TESTING FAILED - Some tests did not pass
```

## Viewing Results in Databricks UI

1. Navigate to **Workflows** in the Databricks workspace
2. Find `integration_tests_dev` or `integration_tests_prod` (the deployed job name)
3. Click on the latest run
4. View the notebook output for detailed test results
5. Check logs for any errors or warnings

## Adding New Tests

To add new tests to the suite:

1. **Open the test notebook**: `tests/test_workflow.py`

2. **Create a test function**:

```python
def test_my_new_validation():
    """Test description"""
    spark = SparkSession.builder.getOrCreate()
    
    # Your test logic here
    # Use assertions to validate
    assert condition, "Error message if condition fails"
    
    print("   ✓ Validation passed")
```

3. **Call the test using run_test helper**:

```python
run_test("Test 5: My New Validation", test_my_new_validation)
```

4. **Deploy and test**:

```bash
databricks bundle deploy --target dev
databricks bundle run integration_tests --target dev
```

## Test Data Cleanup

Tests use the same data paths as the main workflow:
- `/tmp/dab_demo/prepared_data`
- `/tmp/dab_demo/analysis_results/`

These paths are overwritten on each run, so no manual cleanup is needed.

For persistent test data, consider:
- Using environment-specific paths
- Adding cleanup tasks to workflows
- Using test-specific data directories

## Troubleshooting

### Test Job Not Found

**Problem**: `integration_tests_dev` job doesn't exist (in Databricks UI)

**Solution**:
```bash
# Re-deploy the bundle to create all resources
databricks bundle deploy --target dev
```

Note: The resource key is `integration_tests`, but it deploys with the name `integration_tests_dev`.
```bash
databricks bundle deploy --target dev
databricks bundle run demo_workflow --target dev
databricks bundle run integration_tests --target dev
```

### Tests Fail Immediately

**Problem**: Tests fail before validating data

**Solution**:
- Ensure main workflow completed successfully
- Check that data paths match between workflow and tests
- Verify cluster can access data locations

### Timeout Errors

**Problem**: Tests timeout before completing

**Solution**:
- Increase `timeout_seconds` in `resources/test_workflow.yml`
- Check cluster sizing (may need more resources)
- Verify network connectivity to data sources

### Permission Errors

**Problem**: Tests can't read/write data

**Solution**:
- Verify workspace permissions
- Check Unity Catalog permissions (if using UC)
- Ensure service principal has correct access (for prod)

## Best Practices

1. **Run tests after every deployment** - Catch issues early
2. **Review test output** - Don't just check pass/fail status
3. **Update tests when changing workflows** - Keep tests in sync with code
4. **Add tests for new features** - Maintain test coverage
5. **Use meaningful assertions** - Clear error messages help debugging
6. **Test data quality** - Validate business rules and constraints
7. **Monitor test performance** - Keep tests fast for quick feedback
8. **Document test scenarios** - Help team understand what's tested

## CI/CD Integration

### GitHub Actions

See `.github-workflows-example.yml` for a complete example.

Key steps:
1. Validate bundle on all PRs
2. Deploy and test on develop branch
3. Deploy and test on main (production)
4. Fail pipeline if tests fail

### Azure DevOps

```yaml
trigger:
  branches:
    include:
      - main
      - develop

stages:
  - stage: Validate
    jobs:
      - job: ValidateBundle
        steps:
          - script: databricks bundle validate

  - stage: DeployDev
    dependsOn: Validate
    jobs:
      - job: DeployAndTest
        steps:
          - script: databricks bundle deploy --target dev
          - script: databricks bundle run demo_workflow --target dev
          - script: databricks bundle run integration_tests --target dev
```

### GitLab CI

```yaml
stages:
  - validate
  - deploy
  - test

validate:
  stage: validate
  script:
    - databricks bundle validate

deploy_dev:
  stage: deploy
  script:
    - databricks bundle deploy --target dev
  only:
    - develop

test_dev:
  stage: test
  script:
    - databricks bundle run demo_workflow --target dev
    - databricks bundle run integration_tests --target dev
  only:
    - develop
```

## Advanced Topics

### Parameterized Tests

Add parameters to your test workflows:

```yaml
# In resources/test_workflow.yml
tasks:
  - task_key: run_integration_tests
    notebook_task:
      notebook_path: ../tests/test_workflow.py
      base_parameters:
        data_path: "/tmp/dab_demo"
        min_records: "10"
```

### Test Data Generation

For more complex testing, consider:
- Separate test data generation notebooks
- Mock data generators
- Snapshot testing against known good data

### Performance Testing

Add performance validations:

```python
def test_workflow_performance():
    """Ensure workflow completes within SLA"""
    import time
    start = time.time()
    
    # Run workflow or check last run time
    
    duration = time.time() - start
    assert duration < 300, f"Workflow took {duration}s (max: 300s)"
```

### Custom Test Reports

Generate custom reports:

```python
# Save test results to Delta table
test_results_df = spark.createDataFrame(test_results, 
    ["test_name", "status", "error"])
test_results_df.write.format("delta").mode("append") \
    .save("/tmp/dab_demo/test_results")
```

## Summary

The integrated testing framework provides:
- ✅ Automated validation of pipeline correctness
- ✅ Data quality checks
- ✅ End-to-end workflow testing
- ✅ Easy CI/CD integration
- ✅ Detailed test reporting
- ✅ Fast feedback on issues

By running tests consistently after every deployment, you can catch issues early and maintain confidence in your data pipelines.

