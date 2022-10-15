#!/usr/bin/env bash
set -e
set -o pipefail

REPO_ROOT=$(git rev-parse --show-toplevel)

# shellcheck source=/dev/null
source "$REPO_ROOT"/.venv/bin/activate

echo "black:"
time black --check --diff spendthrift tests
echo

echo "isort:"
time isort --check --diff spendthrift tests
echo

echo "mypy:"
time mypy spendthrift tests
echo

echo "pylint:"
time pylint spendthrift tests
