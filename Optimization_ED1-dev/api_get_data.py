import requests
import json as _json
import ast
import joblib

import os
from os.path import dirname, abspath
import psutil

import api_notification


url_folder = dirname(abspath(__file__))
def get_data():
    scenario_id = joblib.load('scenario_id.pkl')
    url = f'https://trainerplusapi.blueskycreations.com.au/api/traininghours?scenario_id={scenario_id}&=#'
    json = {"Content-Type" :"application/json", "apikey" :"N!k3!Bl^ESKY!INT@DGRVHB"}
    print(url)
    api_notification.noti("Get data: Start...")
    x = requests.get(url, headers = json)
    # print(x.text)
    output = x.text

    file = open(url_folder + "/get_output.json", "w")
    file.write(output)
    file.close()
    print("GETFILE DONE")
    api_notification.noti("Get data: Done!")
    return True