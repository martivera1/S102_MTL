#!/bin/bash
service mariadb start

# Wait for the MariaDB server to start up
sleep 10

# Create the database
mysql -u root -e "CREATE DATABASE IF NOT EXISTS pianoclassification;"

export PYTHONPATH=/api

# Run the Flask application
exec "$@"