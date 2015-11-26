import util.building
import datetime


def gethistoricaldata(bid, startdate, daysago):
    start = startdate - datetime.timedelta(days=daysago)
    stop = start + datetime.timedelta(days=1)

    return util.building.getdata(bid, start, stop)


def getaverage(bid, startdate, maxtimeframes, timeframe):
    timeframesago = 0
    datasets = []
    for i in xrange(maxtimeframes):
        timeframesago += 1
        data = gethistoricaldata(bid, startdate, timeframesago * timeframe)

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
