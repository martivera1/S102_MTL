#!/bin/sh

# Wait for the MariaDB server to be ready
while ! mysqladmin ping -h"$MYSQL_HOST" --silent; do
    sleep 1
done

# Create the database if it doesn't exist
mysql -h"$MYSQL_HOST" -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" -e "CREATE DATABASE IF NOT EXISTS $MYSQL_DATABASE;"

# Check if the database is empty and import the SQL script if it is
TABLE_COUNT=$(mysql -h"$MYSQL_HOST" -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" -D "$MYSQL_DATABASE" -e "SHOW TABLES;" | wc -l)
if [ "$TABLE_COUNT" -eq 0 ]; then
    mysql -h"$MYSQL_HOST" -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" "$MYSQL_DATABASE" < /api/db/pianoclassification.sql
fi

# Export necessary environment variables
export PYTHONPATH=/api

# Run the Flask application
exec "$@"