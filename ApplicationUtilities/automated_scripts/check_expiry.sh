#!/bin/bash

# Configuration
APPLICATION_PATH=${1:?Error: Project directory path is required}

# Construct file paths based on APPLICATION_PATH
CERT_FILE="$APPLICATION_PATH/cert.pem"

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

# Main logic to check certificate expiry

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