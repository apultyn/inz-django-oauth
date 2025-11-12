#!/bin/bash
uv run manage.py migrate --noinput
mysql -h '127.0.0.1' -P 3306 -u 'root' -p -D 'django-jwt-db' < scripts/sample_data.sql