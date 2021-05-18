

from get_data import get_data
from data_input import get_excel, get_base_rate
from prepare import date_to_str
base_rate = get_base_rate()
def get_maxot1(_type):
    if _type == "Casual":
        maxot_1 = 10
    elif _type == "Full Time" or _type == "Part Time":
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
                

            elif total_hour >= 40:
                payment = base_rate*(max(_hour,3)*_ot2_rate)
            elif total_hour + min(_hour,maxot_1) >  38:
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