#!/bin/bash
service mariadb start

# Wait for the MariaDB server to start up
sleep 5

# Create the database
mysql -u root -e "CREATE DATABASE IF NOT EXISTS pianoclassification;"

# Alter root user authentication mechanism
mysql -u root -e "ALTER USER 'root'@'localhost' IDENTIFIED VIA mysql_native_password USING PASSWORD('root');"

# Import the SQL script to create tables
mysql -u root -proot pianoclassification < /api/db/pianoclassification.sql

export PYTHONPATH=/api

# Run the Flask application
exec "$@"