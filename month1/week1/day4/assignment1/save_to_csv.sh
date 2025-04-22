#!/usr/bin/bash

echo "Shell is reached"
log_file_csv_path="${1}/sensor_data.csv"
echo "Save $2 to ${log_file_csv_path}"
echo "$2" >> "$log_file_csv_path"

