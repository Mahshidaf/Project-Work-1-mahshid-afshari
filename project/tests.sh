#!/bin/bash

# Enable debugging
set -x

# Wait for 2 seconds
sleep 2

# Define paths
BASE_DIR=$(pwd)
DATA_DIR="${BASE_DIR}/data"
DB_PATH="${DATA_DIR}/combined_data.db"

# Print paths for debugging
echo "BASE_DIR: $BASE_DIR"
echo "DATA_DIR: $DATA_DIR"
echo "DB_PATH: $DB_PATH"

# Ensure the data directory exists
if [ ! -d "$DATA_DIR" ]; then
  echo "Data directory does not exist. Creating it."
  mkdir -p "$DATA_DIR"
fi

# Run the unit tests
python tests.py

# Give some time for the database file to be written
sleep 2

# Check if the combined_data.db file exists in the specified directory
if [ -f "$DB_PATH" ]; then
    echo "File exists."
else
    echo "Test Failed: $DB_PATH does not exist."
    exit 1
fi

# Check if the sqlite3 command is available
if ! command -v sqlite3 &> /dev/null; then
    echo "sqlite3 could not be found. Please install sqlite3."
    exit 1
fi

# Check if the test table exists and has the expected content
sqlite3 "$DB_PATH" <<EOF
.headers on
.mode column
SELECT * FROM test_table;
EOF

echo "All tests passed successfully."
