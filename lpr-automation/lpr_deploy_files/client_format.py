"""
Add `extras` key inside `event` key and add some hard-coded information
"""

def process_event_json_before_sink(event_json):
    if "extras" not in event_json["event"]:
        event_json["event"]["extras"] = {}

    event_json["event"]["extras"] = {
        "device_id": "00:d2:61:b7:58:cc",
        "CamID": "123456",
        "LocationGUID": "74bc7991-f58c-41ab-8edf-2755cc34c25c"
    }

    # json_data['event']['entry_lp']
    if 'entry_lp' in event_json['event']:
        event_json['event']['name'] = event_json['event']['name'].replace(event_json['event']['reading'], event_json['event']['entry_lp'])
        event_json['event']['reading'] = event_json['event']['entry_lp']

    #  changing event Direction to uppercase
    

    return event_json
