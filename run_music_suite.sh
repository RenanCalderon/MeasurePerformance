#! /usr/bin/env bash

APP_TYPE="$1"

if [ -z "$1" ]; then
  echo "Run Music Suite Script"
  python ./music_suite_app.py --log-cli-level='INFO' -vv

elif [ "$1" = "test" ]; then
  echo "Run Music Suite Test"
  export environment=$APP_TYPE
  echo "Environment: $environment"
  TEST="/c/Users/renan/Documents/Python/App/MusicTest/"
  LATEST=$(ls -1 -t $TEST | head -n 1)
  echo "$LATEST"
  FILE="$TEST""$LATEST"/dist/MusicTest.exe
  "$FILE"

elif [ "$1" = "app" ]; then
  echo "Run Music Suite App"
  export environment=$APP_TYPE
  echo "Environment: $environment"
  TEST="/c/Users/renan/Documents/Python/App/MusicSuite/"
  LATEST=$(ls -1 -t $TEST | head -n 1)
  echo "$LATEST"
  FILE="$TEST""$LATEST"/dist/MusicSuite.exe
  "$FILE"

else
  echo "Not valid input"
fi