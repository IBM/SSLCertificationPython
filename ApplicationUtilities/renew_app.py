from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)


@app.route('/deploy', methods=['POST'])
def deploy():
    try:
        # Get application name and path from the POST request body
        data = request.json
        application_name = data.get('application_name')
        application_path = data.get('application_path')

        if not application_name or not application_path:
            return jsonify({"error": "application_name and application_path are required"}), 400

        # Run the deploy.sh script with arguments
        subprocess.run(["/bin/bash", "automated_scripts/deploy2.sh", application_name, application_path], check=True)
        
        return jsonify({"message": f"Deployment of {application_name} successful!"}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"Error during deployment: {str(e)}"}), 500


# # Route to deploy the application
# @app.route('/deploy')
# def deploy():
#     try:
#         # Run the deploy.sh script
#         subprocess.run(["/bin/bash", "automated_scripts/deploy.sh"], check=True)
#         return "Deployment successful!", 200
#     except subprocess.CalledProcessError as e:
#         return f"Error during deployment: {e}", 500
    

# @app.route('/renew_cert', methods=['GET'])
# def renew_cert():
#     try:
#         # Get the validity_days parameter from the query string, default to 5
#         validity_days = request.args.get('validity_days', default=5, type=int)

#         # Call the shell script and pass the validity_days as an argument
#         # script_path = "renew_certificate.sh"
#         result = subprocess.run(
#             ["/bin/bash", "automated_scripts/renew_certificate.sh", str(validity_days)],
#             stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE,
#             text=True
#         )

#         if result.returncode == 0:
#             return jsonify({"message": "Certificate renewal completed successfully!", "output": result.stdout}), 200
#         else:
#             return jsonify({"message": "Certificate renewal failed!", "error": result.stderr}), 500
#     except Exception as e:
#         return jsonify({"message": "An error occurred while renewing the certificate.", "error": str(e)}), 500


@app.route('/renew_cert', methods=['POST'])
def renew_cert():
    try:
        # Extract parameters from JSON request
        data = request.json
        app_name = data.get("application_name")
        validity_days = data.get("validity_days", 5)
        project_dir = data.get("project_dir")

        # Ensure required parameters exist
        if not app_name or not project_dir:
            return jsonify({"status": "error", "message": "Missing required parameters"}), 400

        # Run the Bash script as a subprocess
        result = subprocess.run(
            ["/bin/bash", "automated_scripts/renew_certificate.sh", app_name, str(validity_days), project_dir],
            capture_output=True,
            text=True
        )

        # Check if the script failed
        if result.returncode != 0:
            return jsonify({"status": "error", "message": result.stderr.strip()}), 500

        return jsonify({"status": "success", "message": result.stdout.strip()})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Endpoint to check certificate expiry
@app.route('/check_cert_expiry', methods=['GET', 'POST'])
def check_cert_expiry():
    try:
        # Extract parameters from JSON request
        data = request.json
        project_dir = data.get("project_dir")

        # Ensure required parameters exist
        if not project_dir:
            return jsonify({"status": "error", "message": "Missing project_dir as parameters"}), 400

        # Run the bash script to check certificate expiry
        result = subprocess.run(
            ["/bin/bash", "automated_scripts/check_expiry.sh", project_dir],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Print the output to the terminal (for debugging/logging purposes)
        print(result.stdout)

        # Check if the script ran successfully
        if result.returncode == 0:
            # Here we assume the script outputs two lines: one for expiry date and another for days to expiry
            lines = result.stdout.strip().split("\n")
            print(lines)
            expiry_date = lines[-2].split(": ")[1]  # Extract expiry date from the first line
            days_to_expiry = lines[-1].split(": ")[1]  # Extract days to expiry from the second line

            # Return a success response with the extracted details
            return jsonify({
                "status": "success",
                "message": f"Certificate Expiry Date: {expiry_date}, Days to Expiry: {days_to_expiry}"
            }), 200
        else:
            # If there's an error in the script, return the error message
            return jsonify({
                "status": "error",
                "message": result.stderr.strip()  # Capture any error output from the script
            }), 500

    except Exception as e:
        # Return any unexpected errors
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8081)
