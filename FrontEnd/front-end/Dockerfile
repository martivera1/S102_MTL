# Use an official Node runtime as a parent image
FROM node:16-alpine

# Set the working directory in the container
WORKDIR /front-end

# Install http-server to serve the build folder with HTTPS
RUN npm install -g http-server

# Copy the current directory contents into the container at /front-end
COPY . /front-end

# Install any needed packages
RUN npm install

# Build the app for production
RUN npm run build

# Make port 3000 available to the world outside this container
EXPOSE 3000

# Serve the build folder with HTTPS when the container launches
CMD ["http-server", "build", "-p", "3000", "--ssl", "--cert", "cert/pianomusic.com.crt", "--key", "cert/pianomusic.com.key"]
