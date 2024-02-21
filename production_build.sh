#!/bin/bash

# Build the project
echo "Building the project..."
python3.8 -m pip install -r requirements.txt

echo "Make Migration..."
python3.8 manage.py makemigrations --noinput
python3.8 manage.py migrate --noinput

echo "Collect Static Files..."
python3.8 manage.py collectstatic --noinput