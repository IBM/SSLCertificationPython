#!/bin/bash

# Usage: ./renew_certificate.sh <application_name> <validity_days> <application_path>

# # Configuration
# Accept arguments with default values
APPLICATION_NAME=${1:?Error: Application name is required}  # Mandatory argument
VALIDITY_DAYS=${2:-5}  # Number of days the certificate should be valid (default: 5)
APPLICATION_PATH=${3:?Error: Project directory path is required}  # Mandatory argument

# Construct file paths based on APPLICATION_PATH
CERT_FILE="$APPLICATION_PATH/cert.pem"
KEY_FILE="$APPLICATION_PATH/key.pem"
PODMANFILE="$APPLICATION_PATH/Podmanfile"

# Derived variables
CONTAINER_NAME="$APPLICATION_NAME"
IMAGE_NAME="$APPLICATION_NAME"
THRESHOLD_DAYS=1000  # Renew if the certificate expires within this number of days
PORT_MAPPING="8443:443"  # Static port mapping
# # SHARED_VOLUME="shared-data:/app/data"  # Volume to mount

# Function to check certificate expiry for Linux
check_certificate_expiry_linux() {
    echo "Checking certificate expiry date..."
    EXPIRY_DATE=$(openssl x509 -enddate -noout -in "$CERT_FILE" | sed 's/notAfter=//')
    EXPIRY_TIMESTAMP=$(date -d "$EXPIRY_DATE" +%s)
    CURRENT_TIMESTAMP=$(date +%s)
    DAYS_TO_EXPIRY=$(( (EXPIRY_TIMESTAMP - CURRENT_TIMESTAMP) / 86400 ))
    echo "Certificate expiry date: $EXPIRY_DATE"
    echo "Days to expiry: $DAYS_TO_EXPIRY"
}

# Function to check certificate expiry for macOS
check_certificate_expiry_mac() {
    echo "Checking certificate expiry date..."
    EXPIRY_DATE=$(openssl x509 -enddate -noout -in "$CERT_FILE" | sed 's/notAfter=//')
    # Convert the expiry date to a timestamp
    EXPIRY_TIMESTAMP=$(date -j -f "%b %d %H:%M:%S %Y %Z" "$EXPIRY_DATE" +%s)
    CURRENT_TIMESTAMP=$(date +%s)
    DAYS_TO_EXPIRY=$(( (EXPIRY_TIMESTAMP - CURRENT_TIMESTAMP) / 86400 ))
    echo "Certificate expiry date: $EXPIRY_DATE"
    echo "Days to expiry: $DAYS_TO_EXPIRY"
}


# Function to renew the certificate
renew_certificate() {
    echo "Certificate is nearing expiry. Renewing..."
    openssl req -x509 -nodes -days "$VALIDITY_DAYS" -newkey rsa:2048 -keyout "$KEY_FILE" -out "$CERT_FILE" -subj "/CN=localhost"
    echo "Certificate renewed successfully!"
}

# # Function to stop and remove the existing container
# stop_and_remove_container() {
#     echo "Stopping and removing existing container: $CONTAINER_NAME"
#     podman stop "$CONTAINER_NAME" || true  # Stop container if it's running
#     podman rm -f "$CONTAINER_NAME" || true  # Remove the container forcefully
# }

# Function to stop and remove the existing container, related images, and volumes
stop_and_clean_up() {
    echo "Stopping and removing existing container: $CONTAINER_NAME"
    podman stop "$CONTAINER_NAME" || true  # Stop container if it's running
    podman rm -f "$CONTAINER_NAME" || true  # Remove the container forcefully

    echo "Cleaning up related images..."
    podman rmi -f "$IMAGE_NAME" || true  # Remove the image if it exists

    echo "Cleaning up dangling volumes..."
    podman volume prune -f  # Remove unused volumes
}

# Function to rebuild and restart the container
rebuild_and_restart_container() {
    echo "Building new image: $IMAGE_NAME"
    podman build -t "$IMAGE_NAME" -f "$PODMANFILE"

    echo "Starting new container: $CONTAINER_NAME"
    podman run -d --name "$CONTAINER_NAME" -p "$PORT_MAPPING" "$IMAGE_NAME"
    echo "Container restarted successfully!"
}

# Main logic to manage the certificate

# Check the current OS
OS_TYPE=$(uname)

# Execute the appropriate function based on the OS type
if [[ "$OS_TYPE" == "Darwin" ]]; then
    echo "macOS detected. Using macOS-specific expiry check."
    check_certificate_expiry_mac
elif [[ "$OS_TYPE" == "Linux" ]]; then
    echo "Linux detected. Using Linux-specific expiry check."
    check_certificate_expiry_linux
else
    echo "Unsupported OS detected: $OS_TYPE"
fi

if [ "$DAYS_TO_EXPIRY" -le "$THRESHOLD_DAYS" ]; then
    renew_certificate
    # stop_and_remove_container
    stop_and_clean_up
    rebuild_and_restart_container
else
    echo "Certificate is still valid. No renewal needed."
fi
