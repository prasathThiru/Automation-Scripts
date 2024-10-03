import logging
import csv
#from auth import get_auth
from exec_cmd import send_command
from flask import Flask
import requests  # type: ignore
import re

logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

app = Flask(__name__)
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbGllbnRpZCI6ImZhNmE5OTc1LTE0ZTItNGIwZC1hZjUyLTlmZGVmYWRjMzA3NCIsImV4cCI6MTcyNzc2MTUyNywiaXNzIjoiWEJuRHFDN3U3YnhkV0s5Y2gxaXYwb3laUUF5bXlWSU0ifQ.qqKb0i7d4LHG8M6LL6op63hHG3fAorfzzxR_uIx3m3g"




def get_devices(device_profile_id, count, token):    
    # Logging token for debugging
    logging.debug(f"Using token: {token}")

    headers = {
        'Accept': 'application/json',
        'aicon-jwt': token,  # Ensure the token is passed correctly
        'referer': f'https://monitor.uncannysurveillance.com/deviceProfile/{device_profile_id}/devices'
    }

    body = {
        "search_key": "",
        "sort_by": {"column": "status", "order": "desc"},
        "devices": [],
        "filters": {"dgp": [{"names": ["Demo"]}], "tg": [], "tags": []},
        "filters_op": 0
    }

    try:
        devices_response = requests.get(
            f'{base_url}/dm/api/dm/v1/df2?limit={count}&offset=0&profileType=0',
            headers=headers,
            json=body
        )
        devices_response.raise_for_status()  # Raise error for HTTP 4xx/5xx
        devices_json = devices_response.json()

        count = devices_json['count']
        devices = devices_json['data']
        logging.info(f'Devices retrieved, count: {count}')

        return {device['id']: {'name': device['name'], 'status': device['status']} for device in devices}

    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to retrieve devices: {e}")
        return None

base_url = 'https://monitor.uncannysurveillance.com'
#token = get_auth(10, True)
devices = get_devices('df4b24a3-bbf1-4837-b6fb-5caced1a73c5', 1000, token)

# Ensure devices isn't None before proceeding
if devices:
    with open('output.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Device Name', 'LPR Status'])

        for dev_id, dev_info in devices.items():
            device_id = dev_id
            device_name = dev_info['name']

            api_url = "https://monitor.uncannysurveillance.com"
            cookies = "your-cookies-here"
            headers = {
                'accept': 'application/json, text/plain, */*',
                'content-type': 'application/json;charset=UTF-8',
                'referer': f'https://monitor.uncannysurveillance.com/device/{device_id}/info',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
            }
            
            # Call the send_command function
            response = send_command(device_id, api_url, cookies, headers)
            logging.debug(response)

            try:
                # Extract SD_GPU from the response
                #sd_gpu = re.search(r'"SD_GPU": (\d+)', response['output']).group(1)
                status = re.search(r'"LPR is running fine"', response['output'])
                logging.info(f"{device_name} : {status}")
                writer.writerow([device_name, status])
            except Exception as e:
                writer.writerow([device_name, response])
                logging.error(f"Error processing device {device_name}: {e}")
else:
    logging.error("No devices found. Please check the API call or authentication process.")
    print("Error: No devices were retrieved. Please check the logs for details.")


logging.info("Results exported to output.csv")
print("Results exported to output.csv")

