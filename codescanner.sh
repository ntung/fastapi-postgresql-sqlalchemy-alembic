#!/bin/bash

# 1. Define which directories to exclude (important for memory!)
EXCLUDE_DIRS="./venv|./.venv|./.git|./__pycache__|./build|./dist"

# 2. Gather files carefully, excluding heavy or irrelevant directories
echo "🔍 Gathering Python files..."
FILES=$(find . -name "*.py" | grep -vE "($EXCLUDE_DIRS)")

if [ -z "$FILES" ]; then
    echo "✅ No Python files found to scan."
    exit 0
fi

echo "🚀 Starting analysis..."

# 3. Run Flake8 in batches of 50
# xargs prevents the "Killed: 9" error by limiting memory overhead
echo "--- Running Flake8 ---"
echo "$FILES" | xargs -n 50 flake8 --verbose --count

# 4. Run Pylint in batches of 20
# Pylint is heavier, so we use a smaller batch size
echo "--- Running Pylint ---"
echo "$FILES" | xargs -n 20 pylint --disable=C0114,C0115 # Optional: disable some noise

echo "✅ Analysis complete."