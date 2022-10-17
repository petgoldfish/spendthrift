#!/usr/bin/env bash
set -e
set -o pipefail

REPO_ROOT=$(git rev-parse --show-toplevel)

# shellcheck source=/dev/null
source "$REPO_ROOT"/scripts/utils.sh

# shellcheck source=/dev/null
source "$REPO_ROOT"/.venv/bin/activate

header "pytest:"
time pytest --cov=spendthrift tests
echo
