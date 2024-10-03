import requests  # type: ignore
import json
from time import sleep
import logging

logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

def get_auth(timeout, debug=True, max_retries=3):
    user_credential_json = {
        "name": "uncanny",
        "email": "uncannyvision@aikaan.io",
        "password": "uncannyvision@123456"
    }

    client_header = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Cookie": "aicon-jwt=your-jwt-token"
    }

    url = "https://monitor.uncannysurveillance.com/api/_external/auth/v1/signin"
    retry_count = 0
    token = None

    while retry_count < max_retries:
        try:
            if debug:
                logging.debug(f"Attempting authentication (Retry {retry_count + 1}/{max_retries})")
                logging.debug(f"Credentials: {user_credential_json}")
                logging.debug(f"Headers: {client_header}")
                logging.debug(f"URL: {url}")

            response = requests.post(url, json=user_credential_json, headers=client_header, timeout=timeout)
            response.raise_for_status()  # Raises exception for 4xx/5xx responses

            output_json = response.json()

            if output_json.get("respmsg") == "SUCCESS":
                token = output_json["data"]["token"]
                logging.debug(f"Authentication successful, token: {token}")
                return token

            logging.error(f"Authentication failed: {output_json}")
            retry_count += 1
            sleep(1)  # Wait before retrying

        except requests.RequestException as err:
            logging.error(f"Error during authentication request: {err}")
            retry_count += 1
            sleep(1)
        except json.JSONDecodeError:
            logging.error("Failed to parse response JSON.")
            break
        except KeyError:
            logging.error("Token not found in response.")
            break

    logging.error(f"Authentication failed after {max_retries} attempts.")
    return None

