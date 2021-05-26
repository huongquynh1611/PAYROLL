
from prepare import date_to_str,day_val
from data_input import get_holiday, get_holiday_rate, get_rate_data

holiday_list = get_holiday()
holiday_rate = get_holiday_rate()
rate_data = get_rate_data()
def cal_base_rate(_type, day, start_time, end_time, rate_data,start_date,end_date):
    shift = 2      
    ord_rate = 0
    ot1_rate = 0
    ot2_rate = 0
    if date_to_str(start_date) in holiday_list:
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