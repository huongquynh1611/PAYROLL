from cal_payment import cal_payment
import pandas as pd
import time

_time = time.time()
output = cal_payment().sort_values(['ContactID','Start Period','Start Date']).reset_index(drop=True).to_excel("report_0106.xlsx")
print("Time elapsed: ", time.time() -  _time)
