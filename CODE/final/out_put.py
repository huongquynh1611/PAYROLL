from cal_payment import cal_payment
import pandas as pd
import time

_time = time.time()
output = cal_payment()

result = output.sort_values(['ID','Start Period','Start Date']).reset_index(drop=True)
result = result.to_excel("report_3105_2.xlsx")
print("Time elapsed: ", time.time() -  _time)
