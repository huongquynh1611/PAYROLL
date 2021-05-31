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
def get_base_rate(rate_df,time_df):
    result = pd.merge(time_df, rate_df.dropna(subset=['contactid']), on = 'contactid', how='left', validate='many_to_many')
    result = pd.merge(result, rate_df.dropna(subset=['positionid']), left_on = 'positionid_x', right_on = 'positionid', how='left')
    null_rate = float(rate_df["amount"][rate_df['contactid'].isnull() & rate_df['positionid'].isnull()])
    base_rate = [result['amount_x'][i]if not result['amount_x'].isnull()[i] else (result['amount_y'][i] if not result['amount_y'].isnull()[i] else null_rate) for i in range(len(result['amount_x'])) ]    
    return base_rate