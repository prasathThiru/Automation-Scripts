import json
import requests
import re 
import os
import time
import csv
import logging
#import pandas as pd
#from oauth2client.service_account import ServiceAccountCredentials
#from google.oauth2.service_account import Credentials
#import gspread
#from googleapiclient.discovery import build
#from googleapiclient.errors import HttpError
#from datetime import datetime, timedelta


config_parameter = {}
config_parameter["time_out"] = 100

def get_auth():
    try:
        user_credential_json = {}
        user_credential_json["name"]     = "uncanny"
        user_credential_json["password"] = "uncannyvision@123456"
        user_credential_json["email"]    = "uncannyvision@aikaan.io"

        client_header                 = {}
        client_header["Cookie"]       = "aicon-jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbGllbnRpZCI6ImMwYzY3ZjYyLTU2YTUtNDJhMi1hZjRlLTc1MDBlZjY3MTkwZiIsImV4cCI6MTYwMTk2ODgzMiwiaXNzIjoiaTFoSzg1M2EzOGVxWWgwajBDVFdmbDMyajdJVUJ5alkifQ.soQiAJlGVHtBV_Uez08DjpDRchpF_aVk0zFmubdZxP4"
        client_header["Content-Type"] = "application/json"
        client_header["Accept"]       = "application/json"

        response = requests.post("https://monitor.uncannysurveillance.com/api/_external/auth/v1/signin", json=user_credential_json,headers=client_header,timeout=int(config_parameter["time_out"]))

        print("\tResponse from aikaan authentication : {}\n\n".format(response.text))
        output_json = json.loads(response.text)
        if("respmsg" in output_json.keys()):
            if(output_json["respmsg"] == "SUCCESS"):
                return output_json["data"]["token"]
            else:
                print("Error : ",output_json)
                return output_json
        else:
            print("Error in authentication : {}\n\n".format(output_json["message"]))
            return output_json
    except Exception as err:
        print("Exception in authentication token creation: {}".format(err))
        output_json = {}
        return output_json

def get_device_info(token):
    device_info = []
    url = 'https://monitor.uncannysurveillance.com/dm/api/dm/v1/df2?limit=1000&offset=0&profileType=0'
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json;charset=UTF-8',
        'cookie': "aicon-jwt={}".format(token),
        'origin': 'https://monitor.uncannysurveillance.com',
        'referer': 'https://monitor.uncannysurveillance.com/deviceProfile/6acfea62-b9f9-4126-a34f-2aa657f3eaad/devices',
        'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
    }

    body = {
        "search_key": "",
        "sort_by": {"column": "status", "order": "desc"},
        "devices": [],
        "filters": {"dgp": [{"names": ["FlashParking-LPR"]}], "tg": [], "tags": []},
        "filters_op": 0
    }

    try:
        response = requests.post(url, headers=headers, json=body)
        output_json = json.loads(response.text)
        response.raise_for_status()
        online = 0
        if (int(output_json["count"]) == 0) :
            print("\tNo devices in this profile")
        else:
            for v in (output_json["data"]) :
                device = {}
                device["Device ID"] = v["id"]
               # device["Group"] = v["profilename"]
                device["Device Name"] = v["name"]
               # device["Status"] = 'Active' if v["status"] == 1 else 'Inactive'
               # device["Created At"] = str(v["createdat"])
               # device["Last Seen"] = aikaan_info(token,"https://monitor.uncannysurveillance.com/dm/api/dm/v1/device/{}".format(device["Device ID"]))
              #  print("Last Seen:",device["Last Seen"])
                device_info.append(device)
                if (int(v["status"]) == 1):
                    online = online + 1
        print ("\tTotal device in this profile",int(output_json["count"]))
        print ("\tTotal device online in this profile",int(online))
        return device_info  # Return the JSON response
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        return None

def exec_command(device_id, api_url, cookies, headers):
   
    #url = f"{api_url}/dm/api/dm/v1/device/{device_id}/cmd/be57665d-6431-4e50-8624-5b92700fc837" #Demo profile
    url = f"{api_url}/dm/api/dm/v1/device/{device_id}/cmd/b1253e12-eb07-4621-91df-d4ca24f4723d" #Flashparking-LPR profile check restart command

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


    

# Example usage:

if __name__ == "__main__":
    token = get_auth()
    print(token)
    device_details = get_device_info(token)
    #print(json.dumps(device_details, indent=4))

if device_details:
    with open('fp-lpr-status.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Device Name', 'LPR Status'])

        for dev_info in device_details:  # Assuming device_details is a list of dictionaries
            device_id = dev_info['Device ID']  # Ensure keys match your JSON structure
            device_name = dev_info['Device Name']

            api_url = "https://monitor.uncannysurveillance.com"
            cookies = "aicon-jwt={}".format(token)
            headers = {
                'accept': 'application/json, text/plain, */*',
                'content-type': 'application/json;charset=UTF-8',
                'referer': f'https://monitor.uncannysurveillance.com/device/{device_id}/info',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
            }
            
            # Call the send_command function
            response = exec_command(device_id, api_url, cookies, headers)

            try:
                # Extract status from the response
                status_match = re.search(r'"status":\s*"([^"]+)"', response['output'])
                status = status_match.group(1) if status_match else "Unknown Status"
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