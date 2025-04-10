FROM nginx:alpine

# Copy nginx configuration file
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy the HTML file to the default nginx html directory
COPY ./dist/ /usr/share/nginx/html/

EXPOSE 8080
