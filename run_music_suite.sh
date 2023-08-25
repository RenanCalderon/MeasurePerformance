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
fi
#  if [ ! -x "$FILE" ]; then
#      echo "The file does not have execute permission"
#
#
#      chmod +x "$FILE"
#      if [ $? -eq 0 ]; then
#          echo "Execute permission granted to the file."
#      else
#          echo "Failed to grant execute permission to the file."
#          exit 1
#      fi
#  fi
#
#  "$FILE"
#
#elif [ "$APP_TYPE" = "app" ]; then
#  echo "Run Music Suite App"
#  export environment=$APP_TYPE
#  echo "Environment: $environment"
#else
#  echo "Bad Request"
#fi


