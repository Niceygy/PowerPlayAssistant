#!/bin/bash

clear

# Build the Docker image
docker build -t niceygynet/powerplay_assistant .

# Tag the Docker image (optional)
docker tag niceygynet/powerplay_assistant niceygynet/powerplay_assistant:latest

# Push the Docker image to Docker Hub
docker push niceygynet/powerplay_assistant:latest

#Update local container

cd /opt/stacks/powerplay_assistant

docker compose pull

docker compose down

docker compose up -d
