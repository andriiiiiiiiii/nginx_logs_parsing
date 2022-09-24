#!/bin/bash

python3 nginx_logs_parser.py

current_date=$(date +%Y-%m-%d)
git add nginx_logs_parsed_$current_date.csv
git commit -m "Nginx logs parsed $current_date"