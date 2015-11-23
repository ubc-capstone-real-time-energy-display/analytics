import matplotlib.pyplot as plt
import util.database as database
import sys

def getbid(building):
    c.execute("SELECT bid FROM buildings WHERE name=%s", (building,));
    return c.fetchone()[0];

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

        data2012 = getAvgDataBetween(bid, '2012-01-03', '2012-10-31')
        data2013 = getAvgDataBetween(bid, '2013-01-01', '2013-10-30')
        data2014 = getAvgDataBetween(bid, '2013-12-31', '2014-10-29')

        print len(data2012[0])
        print len(data2013[0])
        print len(data2014[0])

        #plt.plot(data2012[0], data2012[1], 'r', data2012[0], data2013[1], 'g')
        plt.plot(data2012[0], data2012[1], 'r', data2012[0], data2013[1], 'g', data2012[0], data2014[1], 'b')
        #plt.plot(data2012[0], data2012[1], 'r', data2012[0], data2013[1], 'b')

        plt.ylabel("avg kW/15mins")
        plt.xlabel("date (red=2012, green=2013, blue=2014)")
        plt.show()
