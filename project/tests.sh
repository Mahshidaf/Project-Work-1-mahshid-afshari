#!/bin/bash

echo "Setting up test environment !!!"
mkdir -p ./data
rm -f ./data/*.db

echo "Running data pipeline test !!!"
python3 ./project/tests.py  # Ensure this points to the correct file
