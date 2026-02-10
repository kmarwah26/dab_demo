# Databricks Asset Bundle Demo

This project demonstrates a simple Databricks Asset Bundle (DAB) with a workflow containing two sequential tasks.

## Project Structure

```
dab_demo/
├── databricks.yml              # Main DAB configuration file
├── resources/
│   └── workflow.yml           # Workflow resource definition
├── src/
│   ├── task_1_data_preparation.py   # First task notebook
│   └── task_2_data_analysis.py      # Second task notebook
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
- Create the workflow job
- Configure all resources as defined

### 4. Run the Workflow

You can trigger the workflow manually:

```bash
databricks bundle run demo_workflow --target dev
```

Or use the Databricks CLI directly:

```bash
databricks jobs run-now --job-id <job-id>
```

### 5. Monitor the Run

Check the status in the Databricks workspace UI:
- Navigate to **Workflows** in the sidebar
- Find your workflow: `demo_workflow_dev`
- Click on it to view run history and details

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
3. **Use version control** (Git) for your bundle configurations
4. **Set up CI/CD** pipelines for automated deployments
5. **Use service principals** for production deployments
6. **Monitor job runs** and set up appropriate alerts
7. **Document changes** in your notebooks and configurations

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

