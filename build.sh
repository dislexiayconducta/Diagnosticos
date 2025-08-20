#!/usr/bin/env bash
set -o errexit

PROJECT_DIR="/opt/render/project/src/"
STATIC_ROOT="${PROJECT_DIR}/staticfiles"

# cd "$PROJECT_DIR" || { echo "Error: Failed to change to project directory"; exit 1; }

pip install -r requirements.txt

mkdir -p "$STATIC_ROOT"
chmod 755 "$STATIC_ROOT"

# Collect static files
python manage.py collectstatic --noinput --clear

# Apply migrations (if needed)
python manage.py migrate




