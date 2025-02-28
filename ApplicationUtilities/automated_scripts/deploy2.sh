#!/bin/bash

# Usage: ./deploy.sh <application_name> <application_path>

# Get Application Name and Path from Arguments
APPLICATION_NAME="$1"
APPLICATION_PATH="$2"

# Validate Input
if [[ -z "$APPLICATION_NAME" || -z "$APPLICATION_PATH" ]]; then
    echo "Usage: $0 <application_name> <application_path>"
    exit 1
fi

# Ensure Podman Machine Exists and Is Running
PODMAN_MACHINE_NAME="ssl-bee"

if podman machine list --format "{{.Name}}" | grep -q "^$PODMAN_MACHINE_NAME$"; then
    echo "Podman machine $PODMAN_MACHINE_NAME already exists."
else
    echo "Initializing Podman machine $PODMAN_MACHINE_NAME..."
    podman machine init $PODMAN_MACHINE_NAME --cpus 5 --memory 8192 --disk-size 100
    podman machine set --memory 8192 --rootful $PODMAN_MACHINE_NAME
fi

# Start the Podman machine
echo "Starting Podman machine $PODMAN_MACHINE_NAME..."
podman machine start $PODMAN_MACHINE_NAME

# Verify the machine is running
podman machine list

# Clean Up Any Existing Containers with the Same Name
if podman ps -a --format "{{.Names}}" | grep -q "^$APPLICATION_NAME$"; then
    echo "Deleting existing container named $APPLICATION_NAME..."
    podman stop $APPLICATION_NAME
    podman rm -f $APPLICATION_NAME
else
    echo "No existing container named $APPLICATION_NAME found."
fi

# Navigate to the Application Directory
if [[ ! -d "$APPLICATION_PATH" ]]; then
    echo "Error: Application path '$APPLICATION_PATH' does not exist."
    exit 1
fi

cd "$APPLICATION_PATH" || exit

# Build the Local Image
echo "Building the image for $APPLICATION_NAME..."
podman build -t "$APPLICATION_NAME" -f Podmanfile .

# Run the Container
echo "Running the container named $APPLICATION_NAME..."
podman run -d --name "$APPLICATION_NAME" -p 8443:443 "$APPLICATION_NAME"

# Verify the Running Container
podman ps
