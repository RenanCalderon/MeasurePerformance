#! /usr/bin/env bash

export SHELLOPTS
set -o igncr

python -m pytest --log-cli-level='INFO' -vv "$TEST_SCRIPT_FILE"
