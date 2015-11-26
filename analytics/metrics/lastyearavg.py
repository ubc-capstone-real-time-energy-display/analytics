import sys
import util.building
import datetime
import numpy
from dateutil.parser import parse

def _gethistoricaldata(bid, thisyearstart, yearsago, timeframe=364):
    daysago = timeframe * yearsago
    start = thisyearstart - datetime.timedelta(days=daysago)
    stop = start + datetime.timedelta(days=1)

    return util.building.getdata(bid, start, stop)


def _gethistoricalaverage(bid, thisyearstart):
    yearsago = 0
    datasets = []
    for i in xrange(5):
        yearsago += 1
        data = _gethistoricaldata(bid, thisyearstart, yearsago)

        # Extract kwh
        data = [x[1] for x in data]

        if len(data) == 0:
            break
        else:
            datasets.append(data)

    # Make sure dataset lengths are the same
    lens = [len(x) for x in datasets]
    if lens[1:] != lens[:-1]:
        print lens
        print 'Unequal data set lengths (daylight savings or missing data)'
        return

    # Create average
    return [sum(x) / len(x) for x in zip(*datasets)]


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
    y_historicaldata = _gethistoricalaverage(bid, thisyearstart)

    # Convert to cumulative sum
    y_cumsum_thisyear = numpy.cumsum(y_thisyear)
    y_cumsum_historicaldata = numpy.cumsum(y_historicaldata)

    y_visual = [((d[0] - d[1]) / d[1]) * 100 for d in zip(y_cumsum_thisyear, y_cumsum_historicaldata)]

    #return (x, y_thisyear, y_lastyear, y_visual)
    return (x, y_cumsum_thisyear, y_cumsum_historicaldata, y_visual)
