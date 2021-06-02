from cal_payment import cal_payment
from datetime import date
import time

_time = time.time()
today = date.today().strftime("%d%m%y")
output = cal_payment().sort_values(['ContactID','Start Period','Start Date']).reset_index(drop=True).to_excel("report_" + str(today) +".xlsx")
print("Time elapsed: ", time.time() -  _time)
