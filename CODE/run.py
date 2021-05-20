
import time
import pandas as pd
import numpy as np
from pandas import DataFrame
from datetime import datetime


def main(excel_file):


    xls = None
    try:
        xls = pd.ExcelFile(excel_file)
    except:
        print("ERROR: Can not open file!")
        return

    _time = time.time()
    def date_to_str(date):
        date = str(date).split("-")
        return date[1] + "/" + date[2] 

    def day_val(day):
        val = {"Monday":0,"Tuesday":1,"Wednesday":2,'Thursday':3,"Friday":4,"Saturday":5,"Sunday":6}
        return val[day]


    def get_excel():
        time_df = pd.read_excel(xls, 'Time') 
        return time_df

    def get_holiday():

        holiday_df = xls.parse("Holiday")
        holiday_list = [("" if m>9 else "0") + str(m) + "/" + ("" if d>9 else "0") + str(d) for d, m in zip(holiday_df["Day"], holiday_df["Month"])]

        return holiday_list

    def get_holiday_rate():
        holiday_rate = 2.5
        return holiday_rate

    def get_rate_data():
        rate1 = np.array([[1,1.15,1.25,1.5,2],[1,1.15,1.25,1.5,2],[1,1.15,1.25,1.5,2],[1,1.15,1.25,1.5,2],[1,1.15,1.25,1.5,2],[1.5,1.5,1.5,1.5,2],[2,2,2,2,2]])
        rate2 = np.array([[1,1.15,1.25,1.5,2],[1,1.15,1.25,1.5,2],[1,1.15,1.25,1.5,2],[1,1.15,1.25,1.5,2],[1,1.15,1.25,1.5,2],[1.5,1.5,1.5,1.5,2],[2,2,2,2,2]])
        rate3 = np.array([[1.2,1.35,1.45,1.7,2.2],[1.2,1.35,1.45,1.7,2.2],[1.2,1.35,1.45,1.7,2.2],[1.2,1.35,1.45,1.7,2.2],[1.2,1.35,1.45,1.7,2.2],[1.7,1.7,1.7,1.7,2.2],[2.2,2.2,2.2,2.2,2.2]])   
        rate_data = {"fulltime": rate1, "parttime": rate2, "casual": rate3}
        return rate_data
    def get_base_rate():
        base_rate = 20
        return base_rate

    holiday_list = get_holiday()
    holiday_rate = get_holiday_rate()

    rate_data = get_rate_data()
    def cal_base_rate(_type, day, date, start_time, end_time, rate_data,start_date,end_date):
        
        shift = 2;      
        ord_rate = 0
        ot1_rate = 0
        ot2_rate = 0
        if date_to_str(date) in holiday_list:
            ord_rate = holiday_rate
            ot1_rate = holiday_rate
            ot2_rate = holiday_rate
        else:        
            if _type == "fulltime":
                if start_time < 5 or (end_time > 1 and start_date != end_date):
                    shift = 2
                elif end_time > 19 or (end_time < 1 and start_date != end_date):
                    shift = 1
                elif start_time >= 5 and end_time < 20:
                    shift = 0
                
            elif _type == "parttime":
                
                if start_time < 5 or (end_time > 1 and start_date != end_date):
                    shift = 2
                elif end_time > 19 or (end_time < 1 and start_date != end_date):
                    shift = 1
                elif start_time >= 5 and end_time < 20:
                    shift = 0

            else:
                
                if start_time < 5 or (end_time > 1 and start_date != end_date):
                    shift = 2
                elif end_time > 19 or (end_time < 1 and start_date != end_date):
                    shift = 1
                elif start_time >= 5 and end_time < 20:
                    shift = 0
                
            ord_rate = rate_data[_type][day_val(day)][shift]
            ot1_rate = rate_data[_type][day_val(day)][3]
            ot2_rate = rate_data[_type][day_val(day)][4]
            
        return (ord_rate,ot1_rate,ot2_rate,shift)

    base_rate = get_base_rate()

    def get_maxot1(_type):
        if _type == "casual":
            maxot_1 = 10
        elif _type == "fulltime" or _type == "parttime":
            maxot_1 = 8
        return maxot_1

    def cal_pay(_hour,_type, _rate, _ot1_rate, _ot2_rate):
        if _hour <3:
            _hour = 3 
        maxot_1 = get_maxot1(_type)
        return base_rate*(
            min([maxot_1,_hour])*_rate + 
            max([0,min([2,_hour - maxot_1])])*_ot1_rate + 
            max([0,_hour - maxot_1 - 2 ])*_ot2_rate)

    time_df = get_excel()

    def cal_payment():
        file = get_data(time_df)
        period_pay = {} 
        shift_pay = []
        for row in file.iterrows():
            _id          = row[1]["ID"]
            _period      = row[1]["Start Period"] 
            _key_period  = _id + " " + str(_period)
            _hour = row[1]["Hour"]   
            _rate = row[1]["Rate"]
            _ot1_rate = row[1]["Rate OT1"]
            _ot2_rate = row[1]["Rate OT2"]
            _type = row[1]["Type"]
            total_hour = 0
            payment = 0
            maxot_1 = get_maxot1(_type) 
            
            if _key_period in period_pay:        
                total_hour, payment = period_pay[_key_period]

                if total_hour + min(_hour,maxot_1) <= 38:
                    payment = cal_pay(_hour,_type, _rate, _ot1_rate, _ot2_rate)
                elif total_hour >= 40 :
                    payment = base_rate*(max(_hour,3)*_ot2_rate)
                elif total_hour >=38 and total_hour + _hour <40:
                    payment = base_rate*(3*_ot1_rate)

                elif total_hour >=38 and total_hour + _hour >=40: 
                    payment = base_rate*((40-total_hour)*_ot1_rate + (max(_hour,3)+total_hour-40)*_ot2_rate)
                

                elif total_hour + min(_hour,maxot_1)  >  38 and total_hour < 38:
                    ot_hour = (total_hour + _hour) - 38 
            
                    base_hour = 38 - total_hour 
                    
                    base_pay =base_rate*(base_hour *_rate)
                
                    ot_pay = base_rate*(min(2,ot_hour)*_ot1_rate + max(0,ot_hour-2)*_ot2_rate)
                    
                    payment = base_pay + ot_pay
                                    
                total_hour += min(_hour,maxot_1)
                
                period_pay[_key_period] = (total_hour,payment) 
            else: 
                payment = cal_pay(_hour,_type, _rate, _ot1_rate, _ot2_rate)
                
                period_pay[_key_period] = (min(_hour,maxot_1),payment)
            
            shift_pay.append(payment)
            
        file["Pay"] = shift_pay
        return file


    def get_data(time_df):
        import re,math
        data= []
        for row in time_df.iterrows():    
            _id = row[1]["Contact Name"] 
    #         objecttimeid = row[1]['objecttimeid']
    #         parentotid = row[1]['ParentOTID']
    #         if type(parentotid) == float:
    #             parentotid = objecttimeid
        
            start_period = row[1]['Process period start date'].date()   
            start = row[1]["Start date"]
            end   = row[1]["End date"]   
            start_time = start.hour + start.minute/60
            end_time = end.hour + end.minute/60
        
            _type = row[1]["Employment Type"]
            for k in _type.lower().split('\n'):
                _type=re.sub(r"[^a-zA-Z0-9]+",'',k).replace("temporary","")
                
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
                data.append((_id,start_period, start2, end2, start_day2,delta_time2, shift2,_type,rate2,ot1_rate2,ot2_rate2))  
            
            else: 
                delta_time = (end-start).total_seconds() / 3600.0

                    
                rate, ot1_rate, ot2_rate, shift = cal_base_rate(_type, start_day, start_date, start_time, end_time, rate_data,start_date,end_date)
        
                data.append((_id,start_period,start,end, start_day, delta_time,shift,_type, rate,ot1_rate,ot2_rate))
            
        file = pd.DataFrame(data,columns=['ID',"Start Period",'Start Date','End Date',"Day" ,'Hour','Shift',"Type",'Rate',"Rate OT1","Rate OT2"])

        return file


    output = cal_payment()

    result = output.sort_values(['ID','Start Period']).set_index(["ID",'Start Period','Start Date']).drop(["Rate",'Rate OT1','Rate OT2'],1)

    result = result.to_excel("report_2005.xlsx", index = True)
    print("Time elapsed: ", time.time() -  _time)



if __name__ == "__main__":
    excel = input("Excel file path >> ")
    # D:\Quynh\PAYROLL\Input file\Costing Examples_NEW.xlsx
    main(excel)
    input("Enter to exit")