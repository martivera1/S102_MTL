# Use an official Python runtime as a parent image
FROM python:3.10.12 

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV PYTHONPATH=/api
ENV SECRET_KEY '$\x14\x03#Rxa6\xc0\x90j\xd7p\t}\xc3r\xa3_\x11\xa6\xcd;\xff'
ENV MYSQL_ROOT_PASSWORD=root

# Install dependencies
RUN apt-get update && \
    apt-get install -y ffmpeg mariadb-client && \
    apt-get clean

# Set up Flask app
WORKDIR /api
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . /api

# Ensure the SQL script is copied correctly
ADD db/pianoclassification.sql /api/db/pianoclassification.sql

# Create a directory for session files
RUN mkdir -p /api/sessions

# Copy and set permissions for the entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose Flask port
EXPOSE 5000

# Set the entrypoint
ENTRYPOINT ["./entrypoint.sh"]

# Start Flask
CMD ["python", "app.py"]
