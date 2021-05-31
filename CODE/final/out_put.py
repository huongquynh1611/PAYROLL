from cal_payment import cal_payment
import pandas as pd
import time

_time = time.time()
output = cal_payment()

result = output.sort_values(['Employee','Start Period','Start Date'])
result = result.to_excel("report_2705_1.xlsx")
print("Time elapsed: ", time.time() -  _time)
