# Docker Setup for MSM Frontend

This document provides instructions for running the MSM Frontend application using Docker.

## Files Created

1. **Dockerfile**: A two-stage build process that:
   - First stage: Builds the Angular application using Node.js
   - Second stage: Serves the built application using Nginx

2. **docker-compose.yml**: Orchestrates the containers, including:
   - Frontend service (Angular application)
   - Backend service (placeholder configuration)

3. **nginx.conf**: Custom Nginx configuration that:
   - Serves the Angular application
   - Handles Angular routing
   - Proxies API requests to the backend service

## Prerequisites

- Docker installed on your machine
- Docker Compose installed on your machine

## Running the Application

1. **Update the backend configuration**:
   Open `docker-compose.yml` and update the backend service configuration with your actual backend details.

2. **If using a backend image from a tar file**:

   **Option 1: Manual approach**
   Load the image into Docker before starting the containers:
   ```bash
   docker load -i path/to/your-backend-image.tar
   ```

   After loading, you'll see the image name and tag. Update the `image` field in the `docker-compose.yml` file with this information:
   ```yaml
   backend:
     image: actual-backend-image-name:tag
   ```

   **Option 2: Using the helper script**
   Use the provided helper script to automate the process:
   ```bash
   chmod +x load-backend-image.sh
   ./load-backend-image.sh path/to/your-backend-image.tar
   ```

   The script will load the image and automatically update the docker-compose.yml file with the correct image name and tag.

3. **Build and start the containers**:
   ```bash
   docker-compose up -d
   ```

4. **Access the application**:
   Open your browser and navigate to `http://localhost:80`

5. **Stop the containers**:
   ```bash
   docker-compose down
   ```

## Development Workflow

If you want to make changes to the application:

1. Make your changes to the source code
2. Rebuild the Docker image:
   ```bash
   docker-compose build frontend
   ```
3. Restart the containers:
   ```bash
   docker-compose up -d
   ```

## Customization

### Environment Variables

You can customize the environment variables in the `docker-compose.yml` file:

- For the frontend service, update the `environment` section
- For the backend service, uncomment and update the `environment` section

### Volumes

If you need to persist data, uncomment and update the `volumes` section in the `docker-compose.yml` file.

### Ports

If you need to change the ports, update the `ports` section in the `docker-compose.yml` file.
