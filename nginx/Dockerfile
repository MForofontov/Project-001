# Use the official NGINX image as the base image
FROM nginx:latest

# Copy the custom NGINX configuration file
COPY default.conf /etc/nginx/conf.d/default.conf

# Copy SSL certificates
COPY ssl/localhost.pem /etc/nginx/ssl/localhost.pem
COPY ssl/localhost-key.pem /etc/nginx/ssl/localhost-key.pem

# Expose ports
EXPOSE 80
EXPOSE 443

# Start NGINX
CMD ["nginx", "-g", "daemon off;"]
