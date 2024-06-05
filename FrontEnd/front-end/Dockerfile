# Use an official Node runtime as a parent image
FROM node:16-alpine

# Set the working directory in the container
WORKDIR /front-end

# Copy the current directory contents into the container at /app
COPY . /front-end

# Install any needed packages
RUN npm install

# Build the app for production
RUN npm run build

# Install serve to serve the build folder
RUN npm install -g serve

# Make port 3000 available to the world outside this container
EXPOSE 3000

# Serve the build folder when the container launches
CMD ["serve", "-s", "build"]
