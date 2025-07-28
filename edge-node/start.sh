#!/bin/bash

echo "Installing Python Dependencies"
pip3 install -r requirements.txt

echo "Starting Cloud Communication"
python3 main.py
 