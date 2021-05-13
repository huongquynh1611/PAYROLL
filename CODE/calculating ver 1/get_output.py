from pandas import DataFrame
from calculating import solve
import pandas as pd
import time

def output_file():
    data = solve()
    b= pd.DataFrame(data,columns=["Process period start date","Process period end date","Start Date","End Date","Hour","Name","Pay"])
    file = pd.DataFrame(b.groupby(['Name',"Process period start date","Process period end date",'Start Date'])['Pay'].sum(),columns=['Pay'])
    file.to_excel('report_pay.xls', index=True)
    return file

time_run = time.time()
file = output_file()
print("Time elapsed: ", time.time() -  time_run)

