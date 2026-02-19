#!/bin/bash

# Integration Testing Script for DAB Demo
# This script runs the integration tests after deployment

set -e  # Exit on error

echo "=================================================="
echo "DAB Demo - Integration Testing"
echo "=================================================="
echo ""

# Get the target environment (default to dev)
TARGET="${1:-dev}"

echo "Target Environment: $TARGET"
echo ""

# Check if databricks CLI is installed
if ! command -v databricks &> /dev/null; then
    echo "❌ Error: Databricks CLI is not installed"
    echo "Please install it with: pip install databricks-cli"
    exit 1
fi

echo "✅ Databricks CLI found"
echo ""

# Step 1: Deploy the bundle
echo "📦 Step 1: Deploying bundle to $TARGET..."
echo "--------------------------------------------------"
databricks bundle deploy --target "$TARGET"

if [ $? -eq 0 ]; then
    echo "✅ Bundle deployed successfully"
else
    echo "❌ Bundle deployment failed"
    exit 1
fi
echo ""

# Step 2: Run the main workflow
echo "🔄 Step 2: Running main workflow..."
echo "--------------------------------------------------"
databricks bundle run demo_workflow --target "$TARGET"

if [ $? -eq 0 ]; then
    echo "✅ Main workflow completed successfully"
else
    echo "❌ Main workflow failed"
    exit 1
fi
echo ""

# Wait a bit for data to be written
echo "⏳ Waiting for data to be persisted..."
sleep 5
echo ""

# Step 3: Run integration tests
echo "🧪 Step 3: Running integration tests..."
echo "--------------------------------------------------"
databricks bundle run integration_tests --target "$TARGET"

if [ $? -eq 0 ]; then
    echo "✅ Integration tests passed"
else
    echo "❌ Integration tests failed"
    exit 1
fi
echo ""

echo "=================================================="
echo "✅ ALL TESTS COMPLETED SUCCESSFULLY"
echo "=================================================="
echo ""
echo "Summary:"
echo "  - Bundle deployed to: $TARGET"
echo "  - Main workflow executed: demo_workflow (named: demo_workflow_${TARGET})"
echo "  - Integration tests passed: integration_tests (named: integration_tests_${TARGET})"
echo ""

