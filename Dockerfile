FROM python:3.8-slim

# Install dependencies
# RUN apt-get update && apt-get install -y nginx && apt-get clean

# Copy application code
COPY . /home/

WORKDIR /home

# Install Python dependencies
#RUN python3 -m pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy Nginx configuration file
# COPY nginx.conf /etc/nginx/nginx.conf

# Create required directories
# RUN mkdir -p /var/log/nginx /var/run/nginx

# Expose ports
EXPOSE 80

# Start Nginx and Gunicorn
CMD gunicorn -c gunicorn_config.py app:app