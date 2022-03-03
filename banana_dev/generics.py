import requests
import time
import os
import json
from uuid import uuid4
import concurrent.futures


endpoint = 'https://api.banana.dev/'
# Endpoint override for development
if 'BANANA_URL' in os.environ:
    print("Dev Mode")
    if os.environ['BANANA_URL'] == 'local':
        endpoint = 'http://localhost/'
    else:
        endpoint = os.environ['BANANA_URL']
    print("Hitting endpoint:", endpoint)

# THE MAIN FUNCTIONS
# ___________________________________

def api_threader(api_key, call_id):
    while True:
        data = check_api(api_key, call_id)
        if data['message'].lower() == "success":
            return data
        
def run_main(api_key, model_key, model_inputs, strategy):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(start_api, api_key, model_key, model_inputs, strategy)
        call_id = future.result()
        data = executor.submit(api_threader, api_key, call_id)
        return data.result()

def start_main(api_key, model_key, model_inputs, strategy):
    call_id = start_api(api_key, model_key, model_inputs, strategy)
    return call_id

def check_main(api_key, call_id):
    dict_out = check_api(api_key, call_id)
    return dict_out


# THE API CALLING FUNCTIONS
# ________________________

# Takes in start params, returns call ID
def start_api(api_key, model_key, model_inputs, strategy):
    global endpoint
    route_start = "start/v2/"
    url_start = endpoint + route_start

    payload = {
        "id": str(uuid4()),
        "created": time.time(),
        "apiKey" : api_key,
        "modelKey" : model_key,
        "modelInputs" : model_inputs,
        "strategy": strategy,
    }

    response = requests.post(url_start, json=payload)

    if response.status_code != 200:
        raise Exception("server error: status code {}".format(response.status_code))

    try:
        out = response.json()
    except:
        raise Exception("server error: returned invalid json")

    try:
        if "error" in out['message'].lower():
            raise Exception(out['message'])
        call_id = out['callID']
        return call_id
    except:
        raise Exception("server error: Failed to return call_id")

# The bare async checker.
def check_api(api_key, call_id):
    global endpoint
    route_check = "check/v2/"
    url_check = endpoint + route_check
    # Poll server for completed task

    payload = {
        "id": str(uuid4()),
        "created": int(time.time()),
        "longPoll": True,
        "callID": call_id, 
        "apiKey": api_key
    }
    response = requests.post(url_check, json=payload)

    if response.status_code != 200:
        raise Exception("server error: status code {}".format(response.status_code))

    try:
        out = response.json()
    except:
        raise Exception("server error: returned invalid json")

    try:
        if "error" in out['message'].lower():
            raise Exception(out['message'])
        return out
    except Exception as e:
        raise e
