# Fix Applied: Resource Key vs Deployed Name

## The Problem

You encountered this error:
```
Error: resource with key "demo_workflow_dev" not found
```

## Root Cause

**Databricks Asset Bundles have two naming concepts:**

1. **Resource Key** - Used in YAML files and CLI commands
2. **Deployed Name** - The actual name in Databricks workspace

### Example from your config:

```yaml
# resources/workflow.yml
resources:
  jobs:
    demo_workflow:                    # ← Resource key (used in CLI)
      name: demo_workflow_${bundle.target}  # ← Deployed name (shows in UI)
```

## The Fix

Changed all CLI commands from:
```bash
# ❌ WRONG - Using deployed name
databricks bundle run demo_workflow_dev --target dev
databricks bundle run integration_tests_dev --target dev
```

To:
```bash
# ✅ CORRECT - Using resource key
databricks bundle run demo_workflow --target dev
databricks bundle run integration_tests --target dev
```

## Files Updated

1. ✅ `run_tests.sh` - Fixed resource keys in commands
2. ✅ `README.md` - Updated all command examples
3. ✅ `TESTING.md` - Fixed CLI examples
4. ✅ `QUICKSTART_TESTING.md` - Corrected commands
5. ✅ `CHANGES.md` - Updated examples
6. ✅ `PROJECT_STRUCTURE.md` - Fixed references
7. ✅ `.github-workflows-example.yml` - Corrected CI/CD commands

## Key Takeaway

**Always use resource keys with `databricks bundle run`:**

| Command | Use This (Resource Key) | NOT This (Deployed Name) |
|---------|------------------------|--------------------------|
| Main workflow | `demo_workflow` | ~~`demo_workflow_dev`~~ |
| Test workflow | `integration_tests` | ~~`integration_tests_dev`~~ |

**In Databricks UI, you'll see the deployed names:**
- `demo_workflow_dev` (when target=dev)
- `integration_tests_dev` (when target=dev)

## Verification

✅ No linter errors in `databricks.yml`
✅ Bundle structure validated
✅ All documentation updated with correct commands

## Ready to Use

```bash
./run_tests.sh dev
```

This will now work correctly!


