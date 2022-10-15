#!/usr/bin/env bash
set -e
set -o pipefail

REPO_ROOT=$(git rev-parse --show-toplevel)

# shellcheck source=/dev/null
source "$REPO_ROOT"/scripts/utils.sh

header "black:"
black spendthrift tests
echo

header "isort:"
isort spendthrift tests
echo
