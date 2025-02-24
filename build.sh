#!/bin/bash

clear

# Build the Docker image
docker build -t niceygy/powerplayassistant .

# Tag the Docker image (optional)
docker tag niceygy/powerplayassistant ghcr.io/niceygy/powerplayassistant:latest

# Push the Docker image to GH registry
docker push ghcr.io/niceygy/powerplayassistant:latest

#Do the same for EDDataCollector

cd ../collector

docker build -t niceygy/eddatacollector .

docker tag niceygy/eddatacollector ghcr.io/niceygy/eddatacollector:latest

docker push ghcr.io/niceygy/eddatacollector:latest

#Update local container

cd /opt/stacks/powerplay_assistant

docker compose pull

docker compose down

docker compose up -d
