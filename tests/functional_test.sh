#! /usr/bin/env bash

export SHELLOPTS
set -o igncr

# Get the test file name as a command-line argument
TEST_FILE="$1"

# Check if the test file name is provided
if [ -z "$TEST_FILE" ]; then
  # If no test file name is provided, run all test cases
  python -m pytest --log-cli-level='INFO' -vv
else
  # Run pytest with the specified test file
  python -m pytest --log-cli-level='INFO' -vv "$TEST_FILE"
fi
