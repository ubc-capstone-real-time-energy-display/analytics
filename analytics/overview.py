import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import util.database as database
from util.building import getbid
import sys
import datetime

def buildPlotData(rows):
    x = []
    y = []
    for row in rows:
        x.append(row[0])
        y.append(row[1])

    return (x, y)


def getSumDataBetween(bid, dateA, dateB):
    c.execute("SELECT DATE(timestamp) as day, SUM(demand) FROM energy_data WHERE (timestamp BETWEEN %s AND %s) AND bid=%s GROUP BY day", (dateA, dateB, bid))
    rows = c.fetchall()
    return buildPlotData(rows)


def getAvgDataBetween(bid, dateA, dateB):
    c.execute("SELECT DATE(timestamp) as day, AVG(demand) FROM energy_data WHERE (timestamp BETWEEN %s AND %s) AND bid=%s GROUP BY day", (dateA, dateB, bid))
    rows = c.fetchall()
    return buildPlotData(rows)


if __name__ == '__main__':
    db = database.connect("capstone")
    c = db.cursor()

    if len(sys.argv) < 2:
        print "Incorrect usage: python analyze.py [ building name ]"
    else:
        buildingname = sys.argv[1]
        bid = getbid(buildingname)


        # Display data for 2012 - 2014
        year = 0
        start = datetime.datetime(2012, 1, 1)

        # Results
        x = None
        all_y = []

        for i in xrange(3):
            yearstart = start + datetime.timedelta(days=364*year)
            year += 1
            yearstop = start + datetime.timedelta(days=364*year)

            # Generate label
            label = str(yearstart.year)

            # Array of days in the year
            days = []
            for i in xrange(364):
                day = yearstart + datetime.timedelta(i)
                days.append(day)

            if x is None:
                x = days

            # Match data with year
            data = getAvgDataBetween(bid, yearstart, yearstop)
            y = []
            j = 0
            for i in xrange(len(days)):
                if j < len(data[0]) and days[i].date() == data[0][j]:
                    y.append(data[1][j])
                    j += 1
                else:
                    # No data
                    y.append(0)

            all_y.append((label, y))

        # Plot
        for y_data in all_y:
            label, y = y_data
            plt.plot(x, y, label=label)

        # Remove year from x axis
        plt.ylabel("avg kW/15mins")
        plt.xlabel("Date")
        plt.legend(loc='best')
        plt.show()
