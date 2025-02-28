# Ensure Podman Machine Exists and Is Running

# Check if the Podman machine named ssl-bee exists
if podman machine list --format "{{.Name}}" | grep -q "^ssl-bee$"; then
    echo "Podman machine ssl-bee already exists."
else
    echo "Initializing Podman machine ssl-bee..."
    podman machine init ssl-bee --cpus 5 --memory 8192 --disk-size 100
    podman machine set --memory 8192 --rootful ssl-bee
    # podman system connection default ssl-bee-root
fi

# Start the Podman machine
echo "Starting Podman machine ssl-bee..."
podman machine start ssl-bee

# Verify the machine is running
podman machine list

# Clean Up Any Existing Containers with the Same Name (ssl-app)

# # Ensure the Podman socket is connected
# podman system connection default ssl-bee

# Check for existing containers named ssl-app and delete them if found
if podman ps -a --format "{{.Names}}" | grep -q "^ssl-app$"; then
    echo "Deleting existing container named ssl-app..."
    podman stop ssl-app
    podman rm -f ssl-app
    podman rmi -f ssl-app
    podman volume prune -f  # Remove unused volumes

else
    echo "No existing container named ssl-app found."
fi

# Navigate to the directory where Podmanfile and app.py are located
cd '/Users/mohitkashinathnilkute/Documents/Agentic_Workflows/SSLCertificationPython/ApplicationDemo' # Update this path

# Build the Local Image

# Build the image using the specified Podmanfile
echo "Building the image for ssl-app..."
podman build -t ssl-app -f Podmanfile .

# Run the Container

# Run the container named ssl-app, exposing it on port 8080
echo "Running the container named ssl-app..."
podman run -d --name ssl-app -p 8443:443 ssl-app

# Verify the Running Container
podman ps
