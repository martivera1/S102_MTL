#!/bin/sh

# Wait for the MariaDB server to be ready
while ! mysqladmin ping -h"$MYSQL_HOST" --silent; do
    sleep 1
done

# Create the database if it doesn't exist
mysql -h"$MYSQL_HOST" -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" -e "CREATE DATABASE IF NOT EXISTS $MYSQL_DATABASE;"

# Import the SQL script to create tables if the database is empty
if [ ! -f /api/db_initialized ]; then
    mysql -h"$MYSQL_HOST" -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" "$MYSQL_DATABASE" < /api/db/pianoclassification.sql
    touch /api/db_initialized
fi

# Export necessary environment variables
export PYTHONPATH=/api

# Run the Flask application
exec "$@"
