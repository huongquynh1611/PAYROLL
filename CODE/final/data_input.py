import pandas as pd
import numpy as np
xls = pd.ExcelFile("../../Input file/Costing Examples with rates.xlsx")
def get_excel():
    time_df = pd.read_excel(xls, 'Timebands').sort_values(["positionid","contactid"]) 
    return time_df
def get_rate_df():
    rate_df = pd.read_excel(xls, 'Rates').sort_values(["positionid","contactid","effectivedate"])
    return rate_df
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
    rate_df = get_rate_df()
    time_df = get_excel()

    check_null = rate_df["contactid"].isnull() & rate_df["positionid"].isnull()

    amount_list=[]
    
    def foo(row):        
        _contact= row['contactid']
        _position = row['positionid'] 
        _start = row['RoundedStart']        
        rate = 0        
        check_effdate = rate_df["effectivedate"] <= _start
        get_amount = []
        rate = 0
        if isinstance(_position, str):
            check_position = rate_df["positionid"] == _position
            if len(set(check_position))==1: # position not found 
                if isinstance(_contact, str):
                    check_contact = rate_df["contactid"] == _contact
                    if len(set(check_contact))==2: # contact found
                        get_amount = list(rate_df["amount"][check_contact & check_effdate])
                        rate = float(get_amount[-1]) if len(get_amount) > 0 else 0
                    else:
                        get_amount = list(rate_df["amount"][check_null & check_effdate])
                        rate = float(get_amount[-1]) if len(get_amount) > 0 else 0
                else: # contact is null
                    get_amount = list(rate_df["amount"][check_null & check_effdate])                    
                    rate = float(get_amount[-1]) if len(get_amount) > 0 else 0
                        
            else: # position found
                check_contact = rate_df["contactid"] == _contact
                if isinstance(_contact, str): # contact not null
                    if len(set(check_contact))==2: # contact found
                        get_amount = list(rate_df["amount"][check_position & check_contact & check_effdate])
                        if len(get_amount) == 0: # both match but not in the same row
                            get_amount = list(rate_df["amount"][check_position & check_effdate])
                            rate = float(get_amount[-1]) if len(get_amount) > 0 else 0
                        else:
                            rate = float(get_amount[-1])
                            
                    else: # contact not found
                        get_amount = list(rate_df["amount"][check_position & check_effdate])
                        rate = float(get_amount[-1]) if len(get_amount) > 0 else 0
                else: # contact null
                    get_amount = list(rate_df["amount"][check_position & check_effdate])
                    rate = float(get_amount[-1]) if len(get_amount) > 0 else 0
        else: # position is null
            if isinstance(_contact, str): # contact found
                check_contact = rate_df["contactid"] == _contact
                if len(set(check_contact))==2: # contact found
                    get_amount = list(rate_df["amount"][check_contact & check_effdate])
                    rate = float(get_amount[-1]) if len(get_amount) > 0 else 0
                else:
                    get_amount = list(rate_df["amount"][check_null & check_effdate])
                    rate = float(get_amount[-1]) if len(get_amount) > 0 else 0
            else: # contact is null
                get_amount = list(rate_df["amount"][check_null & check_effdate])
                rate = float(get_amount[-1]) if len(get_amount) > 0 else 0
                   
        return rate 
    amount_list = time_df.apply(foo, axis=1)  
    return amount_list
