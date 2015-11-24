import matplotlib.pyplot as plt
import sys
import util.building
import datetime
from dateutil.parser import parse
import numpy


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'Incorrect usage: python diff.py [buildingname] [date (YYYY-MM-DD)] [-s]'
    else:
        # Get arguments
        buildingname = sys.argv[1]
        date = sys.argv[2]
        # Don't show diff, show the two sets of data separately
        separate = len(sys.argv) > 3 and sys.argv[3] == '-s'

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
        plt.gcf().autofmt_xdate()

        # Data
        y_thisyear = [data[1] for data in thisyeardata]
        y_lastyear = [data[1] for data in lastyeardata]

        if separate:
            plt.plot(xaxis, y_thisyear, 'r')
            plt.plot(xaxis, y_lastyear, 'g')
            plt.ylabel("kWh demand")
        else:
            y_cumsum_thisyear = numpy.cumsum(y_thisyear)
            y_cumsum_lastyear = numpy.cumsum(y_lastyear)

            #y = [((d[0] - d[1]) / d[0]) * 100 for d in zip(y_thisyear, y_lastyear)]
            y = [((d[0] - d[1]) / d[0]) * 100 for d in zip(y_cumsum_thisyear, y_cumsum_lastyear)]

            plt.plot(xaxis, y, 'r')
            plt.axhline(0, color='black')
            plt.ylabel("% change")

        plt.xlabel("Time")
        plt.show()
