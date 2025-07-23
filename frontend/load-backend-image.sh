#!/bin/bash
# Script to load a backend Docker image from a tar file and update docker-compose.yml

# Check if the tar file path is provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 <path-to-backend-image.tar>"
    exit 1
fi

TAR_FILE=$1

# Check if the tar file exists
if [ ! -f "$TAR_FILE" ]; then
    echo "Error: File $TAR_FILE does not exist"
    exit 1
fi

echo "Loading Docker image from $TAR_FILE..."
# Load the image and capture the output
LOAD_OUTPUT=$(docker load -i "$TAR_FILE")

# Extract the image name and tag from the output
# The output format is typically: "Loaded image: image-name:tag"
IMAGE_INFO=$(echo "$LOAD_OUTPUT" | grep -o 'Loaded image: .*' | sed 's/Loaded image: //')

if [ -z "$IMAGE_INFO" ]; then
    echo "Error: Could not extract image information from docker load output"
    echo "Raw output: $LOAD_OUTPUT"
    exit 1
fi

echo "Image loaded successfully: $IMAGE_INFO"

# Update the docker-compose.yml file
# This is a simple sed replacement - for more complex cases, consider using a proper YAML parser
sed -i.bak "s|image: your-backend-image-name:tag|image: $IMAGE_INFO|" docker-compose.yml

echo "Updated docker-compose.yml with the loaded image: $IMAGE_INFO"
echo "You can now run 'docker-compose up -d' to start the containers"