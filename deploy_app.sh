#!/bin/bash

APP_TYPE="$1"

DATE=$(date +'%Y%m%d')
NAME="MusicTest"

if [ "$APP_TYPE" = "app" ]; then
  APP_TYPE="main"
  NAME="MusicSuite"
  cd /c/Users/renan/Documents/Python/MusicSuiteApp/$NAME

else
  cd /c/Users/renan/Documents/Python/MusicSuiteApp/$NAME
fi

NEW_DIR="$NAME"_"$DATE"
mkdir -p "$NEW_DIR"
cd "$NEW_DIR"

PROJECT_DIR="/c/Users/renan/Documents/Python/MusicSuite/"

echo "Deployment of Music '$APP_TYPE' "
VENV_DIR="$PROJECT_DIR.venv"

if [ -d "$VENV_DIR" ]; then
    echo "Removing current virtual environment..."
    rm -rf "$VENV_DIR"
fi

echo "Creating a new virtual environment..."
python -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate"
echo "Virtual environment activated '$VENV_DIR' "

pip install -e git+https://github.com/RenanCalderon/Configurations.git@"$APP_TYPE"#egg="$APP_TYPE"

echo "Installing pyinstaller"
pip install pyinstaller

echo "Installing packages"
pip install -r "$PROJECT_DIR/requirements.txt"

echo "Deploying App"
pyinstaller --name "$NAME" --onefile "$PROJECT_DIR/music_suite_app.py"

echo "Removing current virtual environment..."
rm -rf "$VENV_DIR"
echo "Creating a new virtual environment..."
python -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate"
echo "Virtual environment activated '$VENV_DIR' "

pip install -e git+https://github.com/RenanCalderon/Configurations.git@test#egg=test
pip install -r "$PROJECT_DIR/requirements.txt"
