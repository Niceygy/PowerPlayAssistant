FROM python:slim-bullseye

# Install dependencies
# RUN apt-get update && apt-get install -y nginx && apt-get clean

# Copy application code
COPY . /home/

# Set workdir
WORKDIR /home

# Install Python dependencies
RUN pip install -r requirements.txt

# Expose ports
EXPOSE 80

# Start Nginx and Gunicorn
CMD gunicorn -c gunicorn_config.py app:app