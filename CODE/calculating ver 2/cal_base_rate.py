
def cal_base_rate(_type, day, date, start_time, end_time, rate_data):
    from date_to_str import date_to_str
    shift = 2;      
    ord_rate = 0
    ot1_rate = 0
    ot2_rate = 0
    if date_to_str(date) in holiday_list:
        ord_rate = holiday_rate
        ot1_rate = holiday_rate
        ot2_rate = holiday_rate
    else:        
        if _type == "Full Time":
            if start_time < 5 or end_time > 1:
                shift = 2
            elif end_time > 19 or end_time < 1:
                shift = 1
            elif start_time >= 5 and end_time < 20:
                shift = 0
            
        elif _type == "Part Time":
            
            if start_time < 5 or end_time > 1:
                shift = 2
            elif end_time > 19 or end_time < 1:
                shift = 1
            elif start_time >= 5 and end_time < 20:
                shift = 0

        else:
            
            if start_time < 5 or end_time > 1:
                shift = 2
            elif end_time > 19 or end_time < 1:
                shift = 1
            elif start_time >= 5 and end_time < 20:
                shift = 0
            
        ord_rate = rate_data[_type][day_val(day)][shift]
        ot1_rate = rate_data[_type][day_val(day)][3]
        ot2_rate = rate_data[_type][day_val(day)][4]
    return (ord_rate,ot1_rate,ot2_rate)