from util.historicaldata import gethistoricaldata
from util.building import getdata
from numpy import cumsum
from dateutil.parser import parse
from datetime import timedelta

"""
Compare to last month, same day
"""
def run(bid, date):
    today = parse(date)
    tomorrow = today + timedelta(days=1)

    todaydata = getdata(bid, today, tomorrow)
    lastmonthdata = gethistoricaldata(bid, today, 28)

    x = [data[0] for data in todaydata]

    y_today = cumsum([data[1] for data in todaydata])
    y_lastmonth = cumsum([data[1] for data in lastmonthdata])

    y_visual = [((d[0] - d[1]) / d[1]) * 100 for d in zip(y_today, y_lastmonth)]

    return (x, y_today, y_lastmonth, y_visual)
