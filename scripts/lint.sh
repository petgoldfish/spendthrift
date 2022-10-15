#!/usr/bin/env bash
set -e
set -o pipefail

REPO_ROOT=$(git rev-parse --show-toplevel)

# shellcheck source=/dev/null
source "$REPO_ROOT"/scripts/utils.sh

# shellcheck source=/dev/null
source "$REPO_ROOT"/.venv/bin/activate

header "black:"
time black --check --diff spendthrift tests
echo

header "isort:"
time isort --check --diff spendthrift tests
echo

header "mypy:"
time mypy spendthrift tests
echo

header "pylint:"
time pylint spendthrift tests
