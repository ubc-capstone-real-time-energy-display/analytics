import matplotlib.pyplot as plt
import database
import sys

db = database.connect()
c = db.cursor()

def buildPlotData(rows):
    x = []
    y = []
    for row in rows:
        x.append(row[0])
        y.append(row[1])

    return (x, y)


def getSumDataBetween(dateA, dateB):
    c.execute("SELECT DATE(timestamp) as day, SUM(demand) FROM energy_data WHERE (timestamp BETWEEN %s AND %s) GROUP BY day", (dateA, dateB))
    rows = c.fetchall()
    return buildPlotData(rows)


def getAvgDataBetween(dateA, dateB):
    c.execute("SELECT DATE(timestamp) as day, AVG(demand) FROM energy_data WHERE (timestamp BETWEEN %s AND %s) GROUP BY day", (dateA, dateB))
    rows = c.fetchall()
    return buildPlotData(rows)

data2012 = getAvgDataBetween('2012-01-03', '2012-10-31')
data2013 = getAvgDataBetween('2013-01-01', '2013-10-30')
data2014 = getAvgDataBetween('2013-12-31', '2014-10-29')

print len(data2012[0])
print len(data2013[0])
print len(data2014[0])

plt.plot(data2012[0], data2012[1], 'r', data2012[0], data2013[1], 'b', data2012[0], data2014[1], 'g')
#plt.plot(data2012[0], data2012[1], 'r', data2012[0], data2013[1], 'b')

plt.ylabel("avg kW/15mins")
plt.xlabel("date")
plt.show()
