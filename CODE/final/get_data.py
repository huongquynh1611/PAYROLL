from cal_base_rate import cal_base_rate
from prepare import date_to_str

from cal_base_rate import rate_data
from pandas import DataFrame
from datetime import datetime
from data_input import get_holiday
import pandas as pd
import numpy as np

holiday_list = get_holiday()

def get_data(time_df):
    import re
    data= []
    last_data = []
    for row in time_df.iterrows():    
        _id = row[1]["employee_name"] 
        objecttimeid = row[1]['objecttimeid']
        parentotid = row[1]['ParentOTID']
        if type(parentotid) == float:
            parentotid = objecttimeid
        
        start_period = row[1]['PeriodStartDate'].date()   
        start = row[1]["RoundedStart"]
        end   = row[1]["RoundedEnd"]   
        start_time = start.hour + start.minute/60
        end_time = end.hour + end.minute/60
    
        _type = row[1]["employment_type"]
        for k in _type.lower().split('\n'):
            _type=re.sub(r"[^a-zA-Z0-9]+",'',k).replace("temporary","")
            
        start_date = start.date() 
        end_date   = end.date()       
        start_day  = start.strftime('%A')  
            
        if ((start_date != end_date) and ( ((end_time >1) and (start_day in ["Friday","Saturday","Sunday"]))  or ( date_to_str(start_date) in holiday_list or date_to_str(end_date) in holiday_list ) )):     
            delta_time1 = 24 - start_time 
            delta_time2 = end_time      
            # start_date1 = start_date   
            # end_date1= end_date
            # start_date2 = end_date
            # end_date2= end_date
        
            start1= start
            end2=end
            end1= end.replace(hour=0,minute=0)
            start2=end1
            start_day1=start1.strftime('%A')
         
            start_day2=start2.strftime('%A')
            
            data.append((parentotid,start_day1, start1, end1, _type,start_time,0))
            data.append((parentotid,start_day2, start2, end2,_type,0,end_time))  
            last_data.append((_id,start_period,parentotid,objecttimeid, start1, end1,start_day1, _type,delta_time1))
            last_data.append((_id,start_period,parentotid, objecttimeid,start2, end2,start_day2, _type,delta_time2))
            
        else: 
            delta_time = (end-start).total_seconds() / 3600.0
         
            data.append((parentotid,start_day,start,end,_type,start_time,end_time))
            last_data.append((_id,start_period,parentotid, objecttimeid,start, end,start_day, _type,delta_time))
        
    file = pd.DataFrame(data,columns=["ParentOT ID",'Day','Start Date','End Date','Type','Start Time','End Time'])

    for parrent_id in file["ParentOT ID"].unique():
        
        last_end_date = file[file["ParentOT ID"] == parrent_id]['End Date'].iloc[-1]
        last_start_date = file[file["ParentOT ID"] == parrent_id]['Start Date'].iloc[0]

        if  len(file[file["ParentOT ID"] == parrent_id]["Day"].unique())>1      :
            file.loc[file["ParentOT ID"] == parrent_id,"End Date"] = file['End Date']
            file.loc[file["ParentOT ID"] == parrent_id,"Start Date"] = file['Start Date']
        else:
            file.loc[file["ParentOT ID"] == parrent_id,"End Date"] = last_end_date 
            file.loc[file["ParentOT ID"] == parrent_id,"Start Date"] = last_start_date
    
    file['Start Time'] = [i.hour + i.minute/60 for i in file['Start Date']]
    file['End Time'] = [i.hour + i.minute/60 for i in file['End Date']] 

    
    file["Rate"] = [cal_base_rate(
        file['Type'][i],
        file['Day'][i],
        file['Start Time'][i],
        file['End Time'][i], 
        rate_data,file['Start Date'][i].date(),
        file['End Date'][i].date()
        ) for i in range(len(file['Day']))]
    last_file = pd.DataFrame(last_data,columns=["ID",'Start Period','Parent ID','Object ID','Start Date','End Date','Day','Type','Hour'])

    last_file['Rate'] = file["Rate"]
    last_file['Start Date'] = file['Start Date']
    last_file['End Date'] = file['End Date']
    table = pd.DataFrame(last_file).sort_values(["ID",'Start Period','Start Date'])
    return table   
