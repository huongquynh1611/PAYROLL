import datetime
from datetime import timedelta
import time
import pandas as pd
import numpy as np
from datetime import datetime
from create_rate import create_rate
from date_to_str import date_to_str


rate1 = create_rate()[0] # full time
rate2 = create_rate()[1] # part time
rate3 = create_rate()[2] # casual
xls = pd.ExcelFile("D:\Quynh\PAYROLL\Input file\Costing Examples_NEW.xlsx")
time_df = pd.read_excel(xls, 'Time')
holiday_df = xls.parse("Holiday")
list = {"Monday":0,"Tuesday":1,"Wednesday":2,'Thursday':3,"Friday":4,"Saturday":5,"Sunday":6}
holiday_list = [("" if m>9 else "0") + str(m) + "/" + ("" if d>9 else "0") + str(d) for d, m in zip(holiday_df["Day"], holiday_df["Month"])]

def solve():
    base_rate = 20
    holiday_rate = 2.5
    data= []
    # list_pay = []
    for row in time_df.iterrows():    
        _id = row[1]["Contact Name"]    
        ord_rate = 0
        ot1_rate      = 0
        ot2_rate      = 0
        shift = 0
        start_period = row[1]['Process period start date'].date()
        end_period = row[1]['Process period end date'].date()
        start = row[1]["Start date"]
        end   = row[1]["End date"]
        start_time = start.hour
        end_time   = end.hour
        time_ = (end-start).total_seconds() / 3600.0
        type_ = row[1]["Employment Type"]
        start_date = start.date()
        end_date   = end.date()
        start_day  = start.strftime('%A')
        end_day    = end.strftime('%A')
    
        if date_to_str(start_date) in holiday_list:
            ord_rate      = holiday_rate
            ot1_rate      = holiday_rate
            ot2_rate      = holiday_rate        
        else:        
            if type_ == "Full Time":
                if start_time >= 5 and end_time < 20:
                    shift = 0
                elif end_time > 19 or end_time < 1:
                    shift = 1
                elif start_time < 5 or end_time > 1:
                    shift = 2

                ord_rate = rate1[list[end_day]][shift]

                ot1_rate = rate1[list[end_day]][3]
                ot2_rate = rate1[list[end_day]][4]
                
            elif type_ == "Part Time":
                if start_time >= 5 and end_time < 20:
                    shift = 0
                elif end_time > 19 or end_time < 1:
                    shift = 1
                elif start_time < 5 or end_time > 1:
                    shift = 2

                ord_rate = rate2[list[end_day]][shift]

                ot1_rate = rate2[list[end_day]][3]
                ot2_rate = rate2[list[end_day]][4]
            else:
                if start_time >= 5 and end_time < 20:
                    shift = 0
                elif end_time > 19 or end_time < 1:
                    shift = 1
                elif start_time < 5 or end_time > 1:
                    shift = 2
                
                ord_rate = rate3[list[end_day]][shift]

                ot1_rate = rate3[list[end_day]][3]
                ot2_rate = rate3[list[end_day]][4]

        
        pay = base_rate*(min([8,time_])*ord_rate + max([0,min([2,time_ - 8])])*ot1_rate + max([0,min([time_ - 10])])*ot2_rate)   
        # list_pay.append((_id, start,end,shift,end_day,type_, pay))
        
        data.append((start_period,end_period,start_date,end_date,time_,_id,pay))
    return data
solve()