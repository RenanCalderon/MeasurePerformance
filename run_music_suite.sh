#! /usr/bin/env bash

export SHELLOPTS
set -o igncr

export environment="test"
echo "Environment: $environment"

python ./music_suite_app.py --log-cli-level='INFO' -vv