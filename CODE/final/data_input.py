import pandas as pd
import numpy as np
xls = pd.ExcelFile("../../Input file/Costing examples with new condition.xlsx")
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