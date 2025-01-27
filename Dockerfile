FROM python:3.8-slim

# Install dependencies
# RUN apt-get update && apt-get install -y nginx && apt-get clean

# Copy application code
COPY . /home/

WORKDIR /home

#update
# RUN apt update -y

#Install Tools
#apt install curl

# Install Python dependencies
RUN pip install -r requirements.txt

#Create cache

# RUN mkdir /home/cache
RUN touch cache/week1.cache
RUN touch cache/week2.cache
RUN touch cache/week3.cache
RUN touch cache/week4.cache
RUN touch cache/week5.cache
RUN touch cache/week6.cache

# Expose ports
EXPOSE 80

# Start Nginx and Gunicorn
CMD gunicorn -c gunicorn_config.py app:app