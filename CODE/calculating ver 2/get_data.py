
def day_val(day):
    val = {"Monday":0,"Tuesday":1,"Wednesday":2,'Thursday':3,"Friday":4,"Saturday":5,"Sunday":6}
    return val[day]
def get_data(path):
    import os
    import datetime
    from datetime import timedelta
    import time
    import pandas as pd
    import numpy as np
    from pandas import DataFrame
    from datetime import datetime
    from cal_base_rate import cal_base_rate
    xls = pd.ExcelFile(path)
    time_df = pd.read_excel(xls, 'Check')

    holiday_df = xls.parse("Holiday")
    holiday_list = [("" if m>9 else "0") + str(m) + "/" + ("" if d>9 else "0") + str(d) for d, m in zip(holiday_df["Day"], holiday_df["Month"])]

    base_rate = 20
    holiday_rate = 2.5

    rate1 = np.array([[1,1.15,1.25,1.5,2],[1,1.15,1.25,1.5,2],[1,1.15,1.25,1.5,2],[1,1.15,1.25,1.5,2],[1,1.15,1.25,1.5,2],[1.5,1.5,1.5,1.5,2],[2,2,2,2,2]])
    rate2 = np.array([[1,1.15,1.25,1.5,2],[1,1.15,1.25,1.5,2],[1,1.15,1.25,1.5,2],[1,1.15,1.25,1.5,2],[1,1.15,1.25,1.5,2],[1.5,1.5,1.5,1.5,2],[2,2,2,2,2]])
    rate3 = np.array([[1.2,1.35,1.45,1.7,2.2],[1.2,1.35,1.45,1.7,2.2],[1.2,1.35,1.45,1.7,2.2],[1.2,1.35,1.45,1.7,2.2],[1.2,1.35,1.45,1.7,2.2],[1.7,1.7,1.7,1.7,2.2],[2.2,2.2,2.2,2.2,2.2]])   
    rate_data = {"Full Time": rate1, "Part Time": rate2, "Casual": rate3}
    data= []
    list_pay = []
    for row in time_df.iterrows():    
        _id = row[1]["Contact Name"] 
        
        start_period = row[1]['Process period start date'].date()
        end_period = row[1]['Process period end date'].date()
        
        start = row[1]["Start date"]
        end   = row[1]["End date"]   
        start_time = start.hour + start.minute/60
        end_time = end.hour + end.minute/60
            
        _type = row[1]["Employment Type"]
        
        start_date = start.date() 
        end_date   = end.date()
        
        delta_day = int((start_date- end_date).days)
        
        start_day  = start.strftime('%A')
        end_day    = end.strftime('%A')  
        if ((start_date != end_date) and ( ((end_time >=1) and (start_day in ["Friday","Saturday","Sunday"])) or ( date_to_str(start_date) in holiday_list or date_to_str(end_date) in holiday_list ) )):
            
            rate1 = cal_base_rate(_type, start_day, start_date, start_time, 24, rate_data)[0]
            rate2 = cal_base_rate(_type, end_day, end_date, 0, end_time, rate_data)[0]
            ot1_rate1 = cal_base_rate(_type, start_day, start_date, start_time, 24, rate_data)[1]
            ot1_rate2 = cal_base_rate(_type, end_day, end_date, 0, end_time, rate_data)[1]
            ot2_rate1 = cal_base_rate(_type, start_day, start_date, start_time, 24, rate_data)[2]
            ot2_rate2 = cal_base_rate(_type, end_day, end_date, 0, end_time, rate_data)[2]
            
            delta_time1 = 24 - start_time   
            delta_time2 = end_time      
            if delta_time1 <3 :
                delta_time1=3
            if delta_time2<3:
                delta_time2=3
            start_date1 = start_date   
            end_date1= end_date
            start_date2 = end_date
            end_date2= end_date
            
            start1= start
            end2=end
            end1= end.replace(hour=0,minute=0)
            start2=end1
            
            start_day1=start1.strftime('%A')
            end_day1=end1.strftime('%A')
            start_day2=start2.strftime('%A')
            end_day2=end2.strftime('%A')
            
            
            
            data.append((_id,start_period,start_date1,start1, end1, start_time, 24 ,start_day1, delta_time1, rate1,ot1_rate1,ot2_rate1))
            data.append((_id,start_period,start_date2, start2, end2,  0, end_time, start_day2,delta_time2, rate2,ot1_rate2,ot2_rate2))  
        
        else: 
            delta_time = (end-start).total_seconds() / 3600.0
            if delta_time <3:
                delta_time = 3
            rate = cal_base_rate(_type, start_day, start_date, start_time, end_time, rate_data)[0]
            ot1_rate = cal_base_rate(_type, start_day, start_date, start_time, end_time, rate_data)[1]
            ot2_rate = cal_base_rate(_type, start_day, start_date, start_time, end_time, rate_data)[2]
            
            data.append((_id,start_period,start_date,start,end, start_time, end_time,start_day, delta_time, rate,ot1_rate,ot2_rate))
                
                
    file = pd.DataFrame(data,columns=['ID',"Start Period",'Start Date','Start','End', "Start Hour", "End Hour","Day",'Hour','Rate',"Rate OT1","Rate OT2"])        

    return file
    
