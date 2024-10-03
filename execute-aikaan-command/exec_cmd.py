import requests
import json

def send_command(device_id, api_url, cookies, headers):
    """
    Sends a command to a device using the Uncanny Surveillance API.

    Args:
        device_id (str): The ID of the device.
        api_url (str): The base URL of the API.
        cookies (str): The authentication cookies.
        headers (dict): The request headers.

    Returns:
        dict: The JSON response from the API or None if an error occurs.
    """
    url = f"{api_url}/dm/api/dm/v1/device/{device_id}/cmd/be57665d-6431-4e50-8624-5b92700fc837"

    try:
        # Perform the API call directly with cookies as part of the headers
        response = requests.post(
            url,
            headers={**headers, 'cookie': cookies},  # Include cookies in headers
            json={}  # Empty payload if required
        )
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)

        # Attempt to parse the response as JSON
        return response.json()
    
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err} - {response.text}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"General error occurred: {req_err}")

    # Return None if an error occurs
    return None

# Example usage (ensure proper headers and cookies are set)
# response = send_command(device_id, api_url, cookies, headers)

