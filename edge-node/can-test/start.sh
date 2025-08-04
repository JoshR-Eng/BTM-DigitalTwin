#!/bin/bash

# Stop script if failure occurs
set -euo pipefail

# Install dependencies
echo "Installing Python Dependencies"
pip3 install -r Scripts/requirements.txt

# Run CAN test
echo "Starting CAN Test..."
python3 can_test.py
 