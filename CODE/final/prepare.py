def date_to_str(date):
    date = str(date).split("-")
    return date[1] + "/" + date[2] 

def day_val(day):
    val = {"Monday":0,"Tuesday":1,"Wednesday":2,'Thursday':3,"Friday":4,"Saturday":5,"Sunday":6}
    return val[day]
