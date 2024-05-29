# Use an official Python runtime as a parent image
FROM python:3.8

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV PYTHONPATH=/api
ENV SECRET_KEY '$\x14\x03#Rxa6\xc0\x90j\xd7p\t}\xc3r\xa3_\x11\xa6\xcd;\xff'

# Install system dependencies
RUN apt-get update && apt-get install -y \
    mariadb-server \
    libmariadb-dev-compat \
    libmariadb-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set up MySQL root password
ENV MYSQL_ROOT_PASSWORD=root

# Set up Flask app
WORKDIR /api
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . /api

# Create a directory for session files
RUN mkdir -p /api/sessions

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose Flask port
EXPOSE 5000

# Add initialization SQL script
ADD db/pianoclassification.sql /docker-entrypoint-initdb.d/

# Set the entrypoint
ENTRYPOINT ["./entrypoint.sh"]

# Start Flask
CMD ["python", "app.py"]
