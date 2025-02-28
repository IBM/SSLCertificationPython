import requests


def ping_deploy(app_name: str, app_path: str):
    """Function to deploy the application by pinging the /deploy route with dynamic parameters."""
    try:
        url = "http://9.109.198.20:8081/deploy"
        payload = {
            "application_name": app_name,
            "application_path": app_path
        }
        headers = {
            "Content-Type": "application/json"
        }
        
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            print("Deployment completed successfully!")
            return "Deployment completed successfully!"
        else:
            print(f"Failed to trigger deployment: {response.status_code} - {response.text}")
            return f"Failed to trigger deployment: {response.status_code} - {response.text}"
    except Exception as e:
        print(f"Error while pinging /deploy: {e}")
        return f"Error while pinging /deploy: {e}"


# def ping_deploy():
#     """Function to deploy the application by pinging the /deploy route."""
#     try:
#         response = requests.get("http://9.109.198.20:8081/deploy")
#         if response.status_code == 200:
#             print("Deployment Completed successfully!")
#             return "Deployment Completed successfully!"
#         else:
#             print(f"Failed to trigger deployment: {response.status_code} - {response.text}")
#             return f"Failed to trigger deployment: {response.status_code} - {response.text}"
#     except Exception as e:
#         print(f"Error while pinging /deploy: {e}")
#         return f"Error while pinging /deploy: {e}"
    
    
# def ping_renew_cert(validity_days: int) -> str:
#     """
#     Function to renew the SSL certificate and redeploy the application.

#     This function sends a GET request to the `/renew_cert` API endpoint to trigger the certificate renewal process.
#     The `validity_days` parameter is passed as a query parameter to specify the desired validity duration of the new certificate.

#     Args:
#         validity_days (int): The number of days the renewed certificate should be valid.

#     Returns:
#         str: A message indicating the success or failure of the certificate renewal process.
#              - On success: "Certificate renewal completed successfully!"
#              - On failure: An error message containing the HTTP status code and response text or exception details.
#     """
#     try:
#         # Pass validity_days as a query parameter
#         response = requests.get(
#             "http://9.109.198.20:8081/renew_cert",
#             params={"validity_days": validity_days}
#         )

#         if response.status_code == 200:
#             print("Certificate renewal completed successfully!")
#             return "Certificate renewal completed successfully!"
#         else:
#             print(f"Failed to trigger certificate renewal: {response.status_code} - {response.text}")
#             return f"Failed to trigger certificate renewal: {response.status_code} - {response.text}"
#     except Exception as e:
#         print(f"Error while pinging /renew_cert: {e}")
#         return f"Error while pinging /renew_cert: {e}"
    


def ping_renew_cert(application_name: str, project_dir: str, validity_days: int = 5) -> str:
    """
    Function to renew the SSL certificate and redeploy the application via the `/renew_cert_1` endpoint.

    This function sends a POST request to the `/renew_cert_1` API endpoint to trigger the certificate renewal process.
    The `application_name`, `validity_days`, and `project_dir` parameters are sent as JSON in the request body.

    Args:
        application_name (str): The name of the application.
        project_dir (str): The path to the project directory.
        validity_days (int, optional): The number of days the renewed certificate should be valid (default: 5).

    Returns:
        str: A message indicating the success or failure of the certificate renewal process.
             - On success: "Certificate renewal completed successfully!"
             - On failure: An error message containing the HTTP status code and response text or exception details.
    """
    try:
        # Define the request payload
        payload = {
            "application_name": application_name,
            "validity_days": validity_days,
            "project_dir": project_dir
        }

        # Send a POST request with JSON data
        response = requests.post(
            "http://9.109.198.20:8081/renew_cert",
            json=payload
        )

        if response.status_code == 200:
            print("Certificate renewal completed successfully!")
            return "Certificate renewal completed successfully!"
        else:
            print(f"Failed to trigger certificate renewal: {response.status_code} - {response.text}")
            return f"Failed to trigger certificate renewal: {response.status_code} - {response.text}"
    except Exception as e:
        print(f"Error while pinging /renew_cert_1: {e}")
        return f"Error while pinging /renew_cert_1: {e}"

    


def ping_check_cert(project_dir: str):
    """
    Sends a POST request to the /check_cert_expiry API endpoint to check the SSL certificate's expiry date.

    This function sends a JSON payload instead of query parameters.

    Args:
        project_dir (str): The directory path of the project.

    Returns:
        dict: A dictionary containing the response JSON if the request is successful.
        None: If the request fails due to a non-200 status code or an exception.
    """
    url = "http://9.109.198.20:8081/check_cert_expiry"
    headers = {"Content-Type": "application/json"}
    data = {"project_dir": project_dir}

    try:
        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 200:
            print("Certificate expiry check completed successfully!")
            print("Response:", response.json()["message"])
            return response.json()
        else:
            print(f"Failed to check certificate expiry: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Error while pinging /check_cert_expiry: {e}")
        return None




# Example usage:
if __name__ == "__main__":
    # Trigger deployment
    ping_deploy()
    
    # Trigger certificate renewal
    ping_renew_cert()
