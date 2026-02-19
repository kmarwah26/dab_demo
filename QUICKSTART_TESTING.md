# Quick Start Guide - Integrated Testing

## TL;DR - Run Tests in 3 Steps

1. **Deploy the bundle**:
   ```bash
   databricks bundle deploy --target dev
   ```

2. **Run the automated test script**:
   ```bash
   ./run_tests.sh dev
   ```

3. **View results** in your terminal or Databricks workspace UI

---

## What Gets Tested?

✅ Data preparation output exists and is correct  
✅ Data quality (no duplicates, valid values)  
✅ Analysis results are generated correctly  
✅ Data consistency across pipeline stages

---

## Testing Options

### Option 1: Full Automation (Recommended)
```bash
./run_tests.sh dev
```
Deploys, runs workflow, and tests everything.

### Option 2: Manual Control
```bash
# Deploy
databricks bundle deploy --target dev

# Run main workflow
databricks bundle run demo_workflow_dev --target dev

# Run tests
databricks bundle run integration_tests_dev --target dev
```

### Option 3: CI/CD Integration
See `.github-workflows-example.yml` for GitHub Actions setup.

---

## Understanding Results

**All tests passed:**
```
✅ ALL TESTS PASSED
Success Rate: 100.0%
```

**Some tests failed:**
```
❌ TESTING FAILED
Success Rate: 50.0%
Failed: 2 ❌
```
Check the detailed output for error messages.

---

## Common Commands

```bash
# Validate configuration
databricks bundle validate

# Deploy to dev
databricks bundle deploy --target dev

# Deploy to prod
databricks bundle deploy --target prod

# Run tests for dev
./run_tests.sh dev

# View job in Databricks UI
# Navigate to: Workflows → integration_tests_dev
```

---

## When to Run Tests?

- ✅ After every deployment
- ✅ Before promoting to production
- ✅ After code changes
- ✅ In CI/CD pipelines
- ✅ On a schedule (optional)

---

## Getting Help

- Full testing guide: `TESTING.md`
- Project README: `README.md`
- View test code: `tests/test_workflow.py`
- Check configuration: `resources/test_workflow.yml`

---

## Test Workflow Names by Environment

- **Dev**: `integration_tests_dev`
- **Prod**: `integration_tests_prod`

Find these in the Databricks workspace under **Workflows**.

