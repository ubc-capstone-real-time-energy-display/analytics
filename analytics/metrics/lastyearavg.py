import util.building
import datetime
from numpy import cumsum
from dateutil.parser import parse
from util.historicaldata import getaverage


"""
This metric works by averaging all historical data on this day and comparing that to the target day

Known issue: A daylight savings day won't work

@return x, y_calcuated, y
"""
def run(bid, date):
    # Setup time frames
    thisyearstart = parse(date)
    thisyearstop = thisyearstart + datetime.timedelta(days=1)

    # Fetch the data
    thisyeardata = util.building.getdata(bid, thisyearstart, thisyearstop)

    x = [data[0] for data in thisyeardata]

    # Extract y axis
    y_thisyear = [data[1] for data in thisyeardata]
    y_historicaldata = getaverage(bid, thisyearstart, 5, 364)

    # Convert to cumulative sum
    y_cumsum_thisyear = cumsum(y_thisyear)
    y_cumsum_historicaldata = cumsum(y_historicaldata)

    y_visual = [((d[0] - d[1]) / d[1]) * 100 for d in zip(y_cumsum_thisyear, y_cumsum_historicaldata)]

    #return (x, y_thisyear, y_lastyear, y_visual)
    return (x, y_cumsum_thisyear, y_cumsum_historicaldata, y_visual)
