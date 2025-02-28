import os
import subprocess
import sys
from datetime import datetime

# def manage_certificate(cert_file, key_file, podmanfile, container_name, image_name, port_mapping, threshold_days=1000, validity_days=5):
def manage_certificate():
    """
    Function to check certificate expiry, renew certificate if nearing expiry, 
    and rebuild/restart the container.
    """

    cert_file = "/Users/mohitkashinathnilkute/Documents/Agentic Workflows/SSLCertificationPython/ApplicationDemo/cert.pem"
    key_file = "/Users/mohitkashinathnilkute/Documents/Agentic Workflows/SSLCertificationPython/ApplicationDemo/key.pem"
    podmanfile = "/Users/mohitkashinathnilkute/Documents/Agentic Workflows/SSLCertificationPython/ApplicationDemo/Podmanfile"
    container_name = "ssl-app"
    image_name = "ssl-app"
    port_mapping = "8443:443"
    threshold_days=1000
    validity_days=5

    # Function to check certificate expiry for Linux
    def check_certificate_expiry_linux(cert_file):
        print("Checking certificate expiry date...")
        expiry_date = subprocess.check_output(
            f"openssl x509 -enddate -noout -in \"{cert_file}\"", shell=True, text=True
        ).strip().replace("notAfter=", "")
        expiry_date_obj = datetime.strptime(expiry_date, "%b %d %H:%M:%S %Y %Z")
        current_date = datetime.now()
        days_to_expiry = (expiry_date_obj - current_date).days
        print(f"Certificate expiry date: {expiry_date}")
        print(f"Days to expiry: {days_to_expiry}")
        return days_to_expiry

    # Function to check certificate expiry for macOS
    def check_certificate_expiry_mac(cert_file):
        print("Checking certificate expiry date...")
        expiry_date = subprocess.check_output(
            f"openssl x509 -enddate -noout -in \"{cert_file}\"", shell=True, text=True
        ).strip().replace("notAfter=", "")
        expiry_date_obj = datetime.strptime(expiry_date, "%b %d %H:%M:%S %Y %Z")
        current_date = datetime.now()
        days_to_expiry = (expiry_date_obj - current_date).days
        print(f"Certificate expiry date: {expiry_date}")
        print(f"Days to expiry: {days_to_expiry}")
        return days_to_expiry

    # Function to renew the certificate
    def renew_certificate(cert_file, key_file, validity_days):
        print("Certificate is nearing expiry. Renewing...")
        subprocess.run(
            f"openssl req -x509 -nodes -days {validity_days} -newkey rsa:2048 -keyout \"{key_file}\" -out \"{cert_file}\" -subj \"/CN=localhost\"",
            shell=True
        )
        print("Certificate renewed successfully!")

    # Function to stop and remove the existing container
    def stop_and_remove_container(container_name):
        print(f"Stopping and removing existing container: {container_name}")
        subprocess.run(f"podman stop {container_name}", shell=True, stderr=subprocess.DEVNULL)
        subprocess.run(f"podman rm -f {container_name}", shell=True, stderr=subprocess.DEVNULL)

    # Function to rebuild and restart the container
    def rebuild_and_restart_container(container_name, image_name, podmanfile, port_mapping):
        print(f"Building new image: {image_name}")
        subprocess.run(f"podman build -t {image_name} -f \"{podmanfile}\"", shell=True)
        print(f"Starting new container: {container_name}")
        subprocess.run(f"podman run -d --name {container_name} -p {port_mapping} {image_name}", shell=True)
        print("Container restarted successfully!")

    # Main logic to manage the certificate
    os_type = os.uname().sysname

    # Execute the appropriate function based on the OS type
    if os_type == "Darwin":
        print("macOS detected. Using macOS-specific expiry check.")
        days_to_expiry = check_certificate_expiry_mac(cert_file)
    elif os_type == "Linux":
        print("Linux detected. Using Linux-specific expiry check.")
        days_to_expiry = check_certificate_expiry_linux(cert_file)
    else:
        print(f"Unsupported OS detected: {os_type}")
        sys.exit(1)

    if days_to_expiry <= threshold_days:
        renew_certificate(cert_file, key_file, validity_days)
        stop_and_remove_container(container_name)
        rebuild_and_restart_container(container_name, image_name, podmanfile, port_mapping)
    else:
        print("Certificate is still valid. No renewal needed.")


# Example of how to call the function
if __name__ == "__main__":
    CERT_FILE = "/Users/mohitkashinathnilkute/Documents/Agentic Workflows/SSLCertificationPython/ApplicationDemo/cert.pem"
    KEY_FILE = "/Users/mohitkashinathnilkute/Documents/Agentic Workflows/SSLCertificationPython/ApplicationDemo/key.pem"
    PODMANFILE = "/Users/mohitkashinathnilkute/Documents/Agentic Workflows/SSLCertificationPython/ApplicationDemo/Podmanfile"
    CONTAINER_NAME = "ssl-app"
    IMAGE_NAME = "ssl-app"
    PORT_MAPPING = "8443:443"
    
    # manage_certificate(CERT_FILE, KEY_FILE, PODMANFILE, CONTAINER_NAME, IMAGE_NAME, PORT_MAPPING, validity_days=100)
    manage_certificate()
