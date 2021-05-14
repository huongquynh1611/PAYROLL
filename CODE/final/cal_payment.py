

from get_data import get_data
from data_input import get_excel, get_base_rate
from prepare import date_to_str
base_rate = get_base_rate()

def cal_pay(_hour, _rate, _ot1_rate, _ot2_rate):
    return base_rate*(
        min([8,_hour])*_rate + 
        max([0,min([2,_hour - 8])])*_ot1_rate + 
        max([0,min([_hour - 10])])*_ot2_rate)

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

        total_hour = 0
        payment = 0
        
        if _key_period in period_pay:        
            total_hour, payment = period_pay[_key_period]

            if total_hour + _hour <= 38:
                payment = cal_pay(_hour, _rate, _ot1_rate, _ot2_rate)
                

            elif total_hour > 38:
                payment = base_rate*(min(2,_hour)*_ot1_rate + max(0,_hour-2)*_ot2_rate)
            elif total_hour + _hour >  38:
                ot_hour = (total_hour + _hour) - 38 
                
                base_hour = 38 - total_hour 
                
                base_pay =base_rate*(base_hour *_rate)
            
                ot_pay = base_rate*(min(2,ot_hour)*_ot1_rate + max(0,ot_hour-2)*_ot2_rate)
                
                payment = base_pay + ot_pay
            
                
            total_hour += _hour
                
            period_pay[_key_period] = (total_hour,payment) 
        else: 
            payment = cal_pay(_hour, _rate, _ot1_rate, _ot2_rate)
            
            period_pay[_key_period] = (_hour,payment)
        
        shift_pay.append(payment)
    
    file["Pay"] = shift_pay
    return file