import requests
import json as _json
import ast

import os
from os.path import dirname, abspath
import psutil
from datetime import datetime



url_folder = dirname(abspath(__file__))
def noti(content):
    import joblib
    scenario_id = joblib.load('scenario_id.pkl')
    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S%Z")
    url = 'https://trainerplusapi.blueskycreations.com.au/api/TPScenarioNotification'
    json = {
        # "Content-Type" :"application/json", 
        "apikey" :"N!k3!Bl^ESKY!INT@DGRVHB", 
    }

    body = [{
        "scenario_id":f"{scenario_id}",
        "NotificationDateTime": str(now),
        "Notification": content
    }]

    print(body)
    x = requests.post(url, headers = json, json = body)
    print(x)
    
    # output = x.text

    # file = open(url_folder + "/get_output.json", "w")
    # file.write(output)
    # file.close()
    # print("GETFILE DONE")
    return True

# noti("test")