#!/bin/bash

clear

# Build the Docker image
docker build -t niceygy/powerplayassistant .

# Tag the Docker image (optional)
docker tag niceygy/powerplayassistant ghcr.io/niceygy/powerplayassistant:latest

# Push the Docker image to GH registry
docker push ghcr.io/niceygy/powerplayassistant:latest

#Update local container

cd /opt/stacks/elite_apps

docker compose pull

docker compose down

docker compose up -d
