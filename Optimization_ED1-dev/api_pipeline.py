import json_skill1, json_skill3, json_skill4, json_get_output
import api_get_data
import json

import pandas as pd
import numpy as np
import os
from os.path import dirname, abspath
import psutil
import time


url_folder = dirname(abspath(__file__))


def pipeline():
    api_get_data.get_data()
    for PRIORITY_TRAINEE in [1,2,4,5]:
        if(json_skill1.solve(PRIORITY_TRAINEE)):
            # if(json_skill2.solve()):
            if(json_skill3.solve(PRIORITY_TRAINEE)):
                if(json_skill4.solve(PRIORITY_TRAINEE)):
                    # json_get_output.solve()
                    # json_get_output.post_result()
                    print("*************************************************")
                    print(f"PIPELINE {PRIORITY_TRAINEE} DONE")
                    print("*************************************************")
    json_get_output.solve()
    json_get_output.post_result()
    return False

start = time.time()
print(start)
pipeline()
print("Time elapsed: ", time.time() - start)

