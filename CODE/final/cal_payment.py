
from get_data import get_data
from data_input import get_excel, get_base_rate
from prepare import date_to_str
base_rate = get_base_rate()
def get_maxot1(_type):
    if _type == "casual":
        maxot_1 = 10
    elif _type == "fulltime" or _type == "parttime":
        maxot_1 = 8
    return maxot_1

def cal_pay(_hour,_type, _rate, _ot1_rate, _ot2_rate):
    maxot_1 = get_maxot1(_type)
    return base_rate*(
        min([maxot_1,_hour])*_rate + 
        max([0,min([2,_hour - maxot_1])])*_ot1_rate + 
        max([0,_hour - maxot_1 - 2 ])*_ot2_rate)

time_df = get_excel()

def cal_payment():
    file = get_data(time_df)
    period_hour = {}
    parent_hour = {}
    
    shift_pay = []
    hour_day_list = {}
    
    for row in file.iterrows():
        _parent = row[1]["Parent ID"]
        _id          = row[1]["ID"]
        _key_parent = _id + " " + str(_parent)
        _hour = row[1]["Hour"]  
        if _key_parent in hour_day_list:
            hour_day_list[_key_parent] += _hour
        else:
            hour_day_list[_key_parent]= _hour
        
    for row in file.iterrows():
        _id          = row[1]["ID"]
        _period      = row[1]["Start Period"] 
        _key_period  = _id + " " + str(_period)
        _hour = row[1]["Hour"]   
        _rate = row[1]["Rate"][0]
        _ot1_rate = row[1]["Rate"][1]
        _ot2_rate = row[1]["Rate"][2]
        _type = row[1]["Type"]
        _parent = row[1]["Parent ID"]
        _object_id = row[1]["Object ID"]
        _key_parent = _id + " " + str(_parent)
        
        payment = 0
        maxot_1 = get_maxot1(_type) 
        

        total_hour_parent = parent_hour[_key_parent] if _key_parent in parent_hour else 0      

        total_hour_period = period_hour[_key_period] if _key_period in period_hour else 0

        if (total_hour_parent + _hour <= maxot_1): 
            _hour_new = _hour + ((3 - hour_day_list[_key_parent]) if list(file[file["Parent ID"] ==_parent]['Object ID'])[-1] == _object_id and hour_day_list[_key_parent] < 3 else 0)

            if total_hour_period + _hour <= 38:
                payment = base_rate * _hour_new * _rate
                
            elif total_hour_period >= 40 :
              
                payment = base_rate * _hour_new * _ot2_rate
                
            elif total_hour_period >=38 and total_hour_period +  _hour < 40:
               
                payment = base_rate * _hour_new * _ot1_rate

            elif total_hour_period >=38 and total_hour_period +  _hour >= 40:  
                payment = base_rate*((40-total_hour_period)*_ot1_rate + (_hour_new + total_hour_period - 40)*_ot2_rate)

            elif total_hour_period + _hour_new  >  38 and total_hour_period < 38:
                ot_hour = (total_hour_period + _hour) - 38 

                base_hour = 38 - total_hour_period 
            

                base_pay = base_rate*(base_hour * _rate)

                ot_pay = base_rate*(min(2,ot_hour)*_ot1_rate + max(0,ot_hour-2)*_ot2_rate)

                payment = base_pay + ot_pay

            total_hour_period += _hour
            total_hour_parent += _hour
            
        else:   
            
            if total_hour_period + min(_hour,maxot_1) <= 38:   

                _hour_new = maxot_1 - total_hour_parent
                _hour_ot = total_hour_parent + _hour - maxot_1
                payment = (_hour_new * _rate + min(2, _hour_ot) * _ot1_rate + max(_hour_ot - 2, 0) * _ot2_rate)*base_rate
                
            elif total_hour_period >= 40 :              
                payment = base_rate*(max(_hour,3)*_ot2_rate)

            elif total_hour_period >=38 and total_hour_period + _hour <40:               
                payment = base_rate*(3*_ot1_rate)

            elif total_hour_period >=38 and total_hour_period + _hour >=40:    
                payment = base_rate*((40-total_hour_period)*_ot1_rate + (max(_hour,3) + total_hour_period-40)*_ot2_rate)

            elif total_hour_period + min(_hour,maxot_1)  >  38 and total_hour_period < 38:
                ot_hour = (total_hour_period + _hour) - 38 

                base_hour = 38 - total_hour_period 
            
                base_pay = base_rate*(base_hour *_rate)

                ot_pay = base_rate*(min(2,ot_hour)*_ot1_rate + max(0,ot_hour-2)*_ot2_rate)

                payment = base_pay + ot_pay
            
            total_hour_period += (maxot_1 - total_hour_parent) if total_hour_parent < maxot_1 else 0
            total_hour_parent += min(_hour,maxot_1) 
        
        parent_hour[_key_parent] = total_hour_parent
      
        period_hour[_key_period] = total_hour_period 
    
        shift_pay.append(payment)
        
    file["Pay"] = shift_pay
    return file