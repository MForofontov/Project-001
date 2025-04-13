# Use an official Node.js runtime as a parent image
FROM node:20

# Set the working directory
WORKDIR /react_frontend_docker

# Install dependencies
COPY package.json package-lock.json ./
RUN npm install

# Copy the rest of the project files
COPY . .

# Expose port 5173 for Vite's development server
EXPOSE 5173

