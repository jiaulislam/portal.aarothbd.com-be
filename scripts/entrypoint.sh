#!/bin/sh
set -e
echo "Starting manage script"
python3 mangae.py migrate
echo "Ending manage script"
exec "$@"
