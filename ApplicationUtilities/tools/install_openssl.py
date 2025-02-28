import subprocess
import os
import tarfile
import urllib.request

def install_openssl_from_source():
    try:
        # Define OpenSSL version and download URL
        openssl_version = "1.1.1u"  # You can change this to a different version if necessary
        openssl_url = f"https://www.openssl.org/source/openssl-{openssl_version}.tar.gz"
        tar_file = f"openssl-{openssl_version}.tar.gz"
        install_dir = "/usr/local/openssl"

        # Download OpenSSL source code
        print(f"Downloading OpenSSL {openssl_version}...")
        urllib.request.urlretrieve(openssl_url, tar_file)

        # Extract the tarball
        print("Extracting OpenSSL source code...")
        with tarfile.open(tar_file, "r:gz") as tar:
            tar.extractall()

        # Navigate to the extracted directory
        os.chdir(f"openssl-{openssl_version}")

        # Configure, make, and install OpenSSL
        print("Configuring OpenSSL...")
        subprocess.run(["./config", f"--prefix={install_dir}"], check=True)

        print("Compiling OpenSSL...")
        subprocess.run(["make"], check=True)

        print("Installing OpenSSL...")
        subprocess.run(["make", "install"], check=True)

        # Clean up by removing the tarball and source directory
        os.chdir("..")
        os.remove(tar_file)
        subprocess.run(["rm", "-rf", f"openssl-{openssl_version}"])

        # Verify the installation
        print("Verifying OpenSSL installation...")
        result = subprocess.run([f"{install_dir}/bin/openssl", "version"], capture_output=True, text=True, check=True)
        print(f"OpenSSL version: {result.stdout.strip()}")

        return "OpenSSL installed from source successfully."

    except subprocess.CalledProcessError as e:
        print(f"Error during OpenSSL installation from source: {e}")
        return f"Error during OpenSSL installation from source: {e}"

# Run the function
install_openssl_from_source()
