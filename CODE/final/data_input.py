import pandas as pd
import numpy as np
xls = pd.ExcelFile("../../Input file/Costing Examples with rates.xlsx")
def get_excel():
    time_df = pd.read_excel(xls, 'Timebands') 
    return time_df
def get_rate_df():
    rate_df = pd.read_excel(xls, 'Rates')
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
    import math
    rate_df = get_rate_df().sort_values(["contactid","positionid","effectivedate"])
    time_df = get_excel().sort_values(["contactid","positionid"])
    base_rates = []
    amount_list=[]
    for row in time_df.iterrows():
        
        _contactidtime = row[1]['contactid']
        _positiontime = row[1]['positionid'] 
        _start = row[1]['RoundedStart']
        if type(_contactidtime)==float and type(_positiontime)==float:
            amount = list(rate_df["amount"][rate_df["contactid"].isnull() & rate_df["positionid"].isnull() & (rate_df["effectivedate"]  <= _start)])
            if (len(amount) == 0):
                amount_list.append(0)
            else:

                amount_list.append(float(amount[-1]))
        else:
            amount = list(rate_df["amount"][((rate_df["contactid"] == _contactidtime) | (rate_df["positionid"] == _positiontime)) & (rate_df["effectivedate"]  <= _start)])

            if (len(amount) == 0):
                amount_list.append(0)
            else:

                amount_list.append(float(amount[-1]) )
    return (amount_list)