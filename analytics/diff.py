import matplotlib.pyplot as plt
import sys
import util.building
import datetime
from dateutil.parser import parse
import numpy


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'Incorrect usage: python diff.py [buildingname] [date (YYYY-MM-DD)]'
    else:
        # Get arguments
        buildingname = sys.argv[1]
        date = sys.argv[2]

        # Building information
        bid = util.building.getbid(buildingname)

        # Setup time frames
        thisyearstart = parse(date)
        thisyearstop = thisyearstart + datetime.timedelta(days=1)
        lastyearstart = thisyearstart - datetime.timedelta(days=364)
        lastyearstop = lastyearstart + datetime.timedelta(days=1)

        # Fetch the data
        lastyeardata = util.building.getdata(bid, lastyearstart, lastyearstop)
        thisyeardata = util.building.getdata(bid, thisyearstart, thisyearstop)

        # Only use the time for x axis
        xaxis = [data[0] for data in thisyeardata]

        # Data
        y_thisyear = [data[1] for data in thisyeardata]
        y_lastyear = [data[1] for data in lastyeardata]

        f, axarr = plt.subplots(2, sharex=True)

        # Subplot A: Separate data
        axarr[0].set_title("%s: %s" % (buildingname, thisyearstart.strftime("%b %d, %Y (%a)")))
        axarr[0].plot(xaxis, y_thisyear, 'r')
        axarr[0].plot(xaxis, y_lastyear, 'g')
        axarr[0].set_ylabel("kWh demand")

        # Subplot B: Diff
        y_cumsum_thisyear = numpy.cumsum(y_thisyear)
        y_cumsum_lastyear = numpy.cumsum(y_lastyear)

        #y = [((d[0] - d[1]) / d[0]) * 100 for d in zip(y_thisyear, y_lastyear)]
        y = [((d[0] - d[1]) / d[0]) * 100 for d in zip(y_cumsum_thisyear, y_cumsum_lastyear)]

        axarr[1].plot(xaxis, y, 'r')
        axarr[1].axhline(0, color='black')
        axarr[1].set_ylabel("% change")
        axarr[1].set_xlabel("Time")

        plt.show()
