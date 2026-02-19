# Databricks Asset Bundle Demo

This project demonstrates a simple Databricks Asset Bundle (DAB) with a workflow containing two sequential tasks.

## Project Structure

```
dab_demo/
├── databricks.yml              # Main DAB configuration file
├── resources/
│   ├── workflow.yml           # Main workflow resource definition
│   └── test_workflow.yml      # Integration test workflow definition
├── src/
│   ├── task_1_data_preparation.py   # First task notebook
│   └── task_2_data_analysis.py      # Second task notebook
├── tests/
│   └── test_workflow.py       # Integration tests
├── run_tests.sh               # Test execution script
└── README.md                  # This file
```

## Workflow Overview

The workflow consists of two tasks:

1. **Task 1: Data Preparation** (`task_1_data_preparation.py`)
   - Generates sample employee data
   - Adds processing timestamp
   - Saves data to Delta table
   - Creates temporary view for next task

2. **Task 2: Data Analysis** (`task_2_data_analysis.py`)
   - Loads prepared data from Task 1
   - Performs various analyses:
     - Employee count by department
     - Age statistics by department
     - Overall statistics
   - Saves analysis results to Delta tables

Task 2 depends on Task 1, so it will only run after Task 1 completes successfully.

## Prerequisites

Before deploying this bundle, ensure you have:

1. **Databricks CLI** installed (version 0.205.0 or later)
   ```bash
   # Install Databricks CLI
   curl -fsSL https://raw.githubusercontent.com/databricks/setup-cli/main/install.sh | sh
   ```

2. **Databricks Workspace** access with appropriate permissions

3. **Authentication** configured (one of the following):
   - OAuth (recommended for personal use)
   - Personal Access Token
   - Service Principal (recommended for CI/CD)

## Configuration

Before deploying, update the `databricks.yml` file:

1. **Development target**:
   ```yaml
   dev:
     workspace:
       host: https://your-workspace.cloud.databricks.com  # Update this
   ```

2. **Production target** (optional):
   ```yaml
   prod:
     workspace:
       host: https://your-workspace.cloud.databricks.com  # Update this
     run_as:
       service_principal_name: "your-service-principal"   # Update this
   ```

3. **Update email notifications** in `resources/workflow.yml`:
   ```yaml
   email_notifications:
     on_failure:
       - your-email@example.com  # Update this
   ```

4. **Adjust cluster configuration** if needed (node types, Spark version, etc.)

## Integrated Testing

This bundle includes comprehensive integration testing that validates your workflow end-to-end after deployment.

### Test Coverage

The integration tests verify:

1. **Data Preparation Output** - Validates that Task 1 produces expected data
2. **Data Quality** - Checks for duplicates, valid values, and schema correctness
3. **Analysis Results** - Verifies Task 2 analysis outputs exist and are correct
4. **Data Consistency** - Ensures consistency between preparation and analysis stages

### Running Tests

#### Option 1: Automated Testing with Script (Recommended)

Use the provided test script for end-to-end deployment and testing:

```bash
# Run tests for dev environment
./run_tests.sh dev

# Run tests for prod environment
./run_tests.sh prod
```

This will:
1. Deploy the bundle to your workspace
2. Run the main workflow
3. Execute integration tests
4. Report results

#### Option 2: Manual Step-by-Step Testing

Run each component individually:

```bash
# 1. Deploy the bundle
databricks bundle deploy --target dev

# 2. Run the main workflow
databricks bundle run demo_workflow_dev --target dev

# 3. Run the integration tests
databricks bundle run integration_tests_dev --target dev
```

#### Option 3: CI/CD Pipeline Integration

For automated testing in CI/CD, see `.github-workflows-example.yml` for a GitHub Actions example that automatically runs tests on every deployment.

### Test Results

Tests will produce detailed output including:
- ✅ Pass/Fail status for each test
- Detailed validation messages
- Summary statistics
- Overall success rate

Example output:
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
```

For detailed testing documentation, see `TESTING.md`.

## Deployment

### 1. Authenticate with Databricks

```bash
databricks auth login --host https://your-workspace.cloud.databricks.com
```

### 2. Validate the Bundle

```bash
databricks bundle validate
```

This checks your configuration for syntax errors and validates resources.

### 3. Deploy to Development

```bash
databricks bundle deploy --target dev
```

This will:
- Upload notebooks to your workspace
- Create the workflow jobs (main + test)
- Configure all resources as defined

### 4. Run and Test the Workflow

Use the test script for automated deployment and testing:

```bash
./run_tests.sh dev
```

Or run workflows manually:

```bash
# Run main workflow
databricks bundle run demo_workflow --target dev

# Run integration tests
databricks bundle run integration_tests --target dev
```

### 5. Monitor the Run

Check the status in the Databricks workspace UI:
- Navigate to **Workflows** in the sidebar
- Find your workflows:
  - `demo_workflow_dev` - Main data pipeline (this is the deployed name)
  - `integration_tests_dev` - Integration tests (this is the deployed name)
- Click on them to view run history and details

## Deployment Targets

This bundle supports multiple deployment targets:

- **dev** (default): Development environment
  - Mode: `development`
  - Allows rapid iteration and testing
  - Uses your personal workspace folder

- **prod**: Production environment
  - Mode: `production`
  - Uses service principal for execution
  - Requires additional permissions
  - Deploys to shared location

Deploy to different targets:

```bash
# Development (default)
databricks bundle deploy --target dev

# Production
databricks bundle deploy --target prod
```

## Making Changes

### Updating Notebooks

1. Edit the Python files in the `src/` directory
2. Run `databricks bundle deploy` to upload changes
3. Test your changes by running the workflow

### Modifying the Workflow

1. Edit `resources/workflow.yml`
2. Update task configurations, dependencies, schedules, etc.
3. Run `databricks bundle validate` to check syntax
4. Run `databricks bundle deploy` to apply changes

### Adding New Tasks

1. Create a new Python notebook in `src/`
2. Add a new task definition in `resources/workflow.yml`
3. Set up dependencies using `depends_on`
4. Deploy the updated bundle

## Cleanup

To remove all deployed resources:

```bash
databricks bundle destroy --target dev
```

**Warning**: This will permanently delete the workflow and all associated resources.

## Useful Commands

```bash
# Validate bundle configuration
databricks bundle validate

# Deploy to specific target
databricks bundle deploy --target dev

# Run a specific workflow
databricks bundle run demo_workflow --target dev

# Run integration tests
databricks bundle run integration_tests --target dev

# Run full test suite (deploy + workflow + tests)
./run_tests.sh dev

# View deployment summary
databricks bundle summary --target dev

# Destroy deployed resources
databricks bundle destroy --target dev

# View bundle documentation
databricks bundle --help
```

## Troubleshooting

### Authentication Issues

If you encounter authentication errors:

```bash
# Re-authenticate
databricks auth login --host https://your-workspace.cloud.databricks.com

# Or set environment variables
export DATABRICKS_HOST="https://your-workspace.cloud.databricks.com"
export DATABRICKS_TOKEN="your-token"
```

### Deployment Failures

- Check that your workspace URL is correct in `databricks.yml`
- Ensure you have permissions to create jobs and clusters
- Validate your bundle: `databricks bundle validate`
- Check the error messages for specific issues

### Job Failures

- View logs in the Databricks workspace UI
- Check cluster logs for startup issues
- Verify node types are available in your workspace
- Ensure Delta table paths are accessible

## Best Practices

1. **Use separate targets** for development and production
2. **Test in dev** before deploying to production
3. **Run integration tests** after every deployment to catch issues early
4. **Use version control** (Git) for your bundle configurations
5. **Set up CI/CD** pipelines for automated deployments with testing
6. **Use service principals** for production deployments
7. **Monitor job runs** and set up appropriate alerts
8. **Document changes** in your notebooks and configurations
9. **Review test results** before promoting to production
10. **Add new tests** when adding new features or tasks

## Additional Resources

- [Databricks Asset Bundles Documentation](https://docs.databricks.com/dev-tools/bundles/index.html)
- [Databricks CLI Documentation](https://docs.databricks.com/dev-tools/cli/index.html)
- [Workflow Configuration Reference](https://docs.databricks.com/workflows/index.html)
- [Delta Lake Documentation](https://docs.databricks.com/delta/index.html)

## Support

For issues or questions:
- Check Databricks documentation
- Review error logs in the workspace UI
- Contact your Databricks administrator
- Open an issue in your project repository

