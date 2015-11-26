import sys
import util.building
import datetime
import numpy
from dateutil.parser import parse

"""
Known issue: A daylight savings day won't work

@return x, y_calcuated, y
"""
def run(bid, date):
    # Setup time frames
    thisyearstart = parse(date)
    thisyearstop = thisyearstart + datetime.timedelta(days=1)
    lastyearstart = thisyearstart - datetime.timedelta(days=364)
    lastyearstop = lastyearstart + datetime.timedelta(days=1)

    # Fetch the data
    lastyeardata = util.building.getdata(bid, lastyearstart, lastyearstop)
    thisyeardata = util.building.getdata(bid, thisyearstart, thisyearstop)

    x = [data[0] for data in thisyeardata]

    # Extract y axis
    y_thisyear = [data[1] for data in thisyeardata]
    y_lastyear = [data[1] for data in lastyeardata]

    # Convert to cumulative sum
    y_cumsum_thisyear = numpy.cumsum(y_thisyear)
    y_cumsum_lastyear = numpy.cumsum(y_lastyear)

    y_visual = [((d[0] - d[1]) / d[1]) * 100 for d in zip(y_cumsum_thisyear, y_cumsum_lastyear)]

    #return (x, y_thisyear, y_lastyear, y_visual)
    return (x, y_cumsum_thisyear, y_cumsum_lastyear, y_visual)
