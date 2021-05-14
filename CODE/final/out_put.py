from cal_payment import cal_payment
import pandas as pd
import time

_time = time.time()
output = cal_payment()


result = output.sort_values(['ID','Start Period']).set_index(["ID",'Start Period','Start Date'])
result = result.to_excel("file_report3.xlsx", index = True)
print("Time elapsed: ", time.time() -  _time)
