#!/bin/bash

# Check if the virtual environment folder exists
# retries=0
# while [ ! -d "/app/venv/bin/" ]; do
#     if [ $retries -ge 5 ]; then
#         echo "Virtual environment not found after 5 retries. Exiting."
#         exit 1
#     fi
#     echo "Virtual environment not found. Retrying in 5 seconds..."
#     retries=$((retries + 1))
#     sleep 5
# done

# Install virtual environment if not already installed
if [ ! -d "/app/venv" ] || [ ! -d "/app/venv/bin" ]; then
    echo "Virtual environment not found. Creating one..."
    python3 -m venv /app/venv
fi

# Install required packages
/app/venv/bin/pip install -r /app/requirements.txt

# Activate the virtual environment
source /app/venv/bin/activate

export COQUI_TOS_AGREED=1

# Run the Python script
python -u /app/main.py