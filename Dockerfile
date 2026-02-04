# Use nginx alpine for a small, production-ready image
FROM nginx:alpine

# Copy custom nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Copy static files to nginx html directory
COPY index.html /usr/share/nginx/html/
COPY data.json /usr/share/nginx/html/
COPY assets/ /usr/share/nginx/html/assets/

# Expose port 8080 (fly.io default)
EXPOSE 8080

# Start nginx in foreground
CMD ["nginx", "-g", "daemon off;"]
