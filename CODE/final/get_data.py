from cal_base_rate import cal_base_rate
from prepare import date_to_str
import datetime
from datetime import timedelta
from cal_base_rate import rate_data
from pandas import DataFrame
from datetime import datetime
from data_input import get_holiday
import pandas as pd

holiday_list = get_holiday()

def get_data(time_df):
    data= []
    for row in time_df.iterrows():    
        _id = row[1]["Contact Name"] 
        
        start_period = row[1]['Process period start date'].date()   
        start = row[1]["Start date"]
        end   = row[1]["End date"]   
        start_time = start.hour + start.minute/60
        end_time = end.hour + end.minute/60
    
        _type = row[1]["Employment Type"]
        
        start_date = start.date() 
        end_date   = end.date()
        
        start_day  = start.strftime('%A')
        end_day    = end.strftime('%A')  
        if ((start_date != end_date) and ( ((end_time >1) and (start_day in ["Friday","Saturday","Sunday"])) or ( date_to_str(start_date) in holiday_list or date_to_str(end_date) in holiday_list ) )):
            
            
            delta_time1 = 24 - start_time   
            delta_time2 = end_time      
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
            
            rate1, ot1_rate1, ot2_rate1, shift1 = cal_base_rate(_type, start_day, start_date, start_time, 0, rate_data,start_date1,end_date1)
            rate2, ot1_rate2, ot2_rate2, shift2 = cal_base_rate(_type, start_day, start_date, 0, end_time, rate_data,start_date2,end_date2)
        
            data.append((_id,start_period,start1, end1, start_day1, delta_time1,shift1,_type, rate1,ot1_rate1,ot2_rate1))
            data.append((_id,start_period, start2, end2, start_day2, delta_time2, shift2,_type,rate2,ot1_rate2,ot2_rate2))  
        
        else: 
            delta_time = (end-start).total_seconds() / 3600.0

                
            rate, ot1_rate, ot2_rate, shift = cal_base_rate(_type, start_day, start_date, start_time, end_time, rate_data,start_date,end_date)
    
            data.append((_id,start_period,start,end, start_day, delta_time,shift,_type, rate,ot1_rate,ot2_rate))
        
    file = pd.DataFrame(data,columns=['ID',"Start Period",'Start Date','End Date',"Day" ,'Hour','Shift',"Type",'Rate',"Rate OT1","Rate OT2"])

    return file