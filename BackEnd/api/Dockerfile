# Use an official Python runtime as a parent image
FROM python:3.8

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Install system dependencies
RUN apt-get update && apt-get install -y \
    mysql-server \
    libmysqlclient-dev

# Set up MySQL root password
ENV MYSQL_ROOT_PASSWORD=root

# Create database (replace dbname with your choice)
RUN service mysql start && mysql -u root -pmy-secret-pw -e "CREATE DATABASE pianoclassification;"

# Set up Flask app
WORKDIR /api
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . /api

# Expose Flask port
EXPOSE 5000

# Add initialization SQL script
ADD db/pianoclassification.sql /docker-entrypoint-initdb.d/

# Start Flask and MySQL
CMD service mysql start && flask run
