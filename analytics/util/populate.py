import os
import sys
import datetime 
import database
from dateutil.parser import parse

##
# USAGE:  python populate.py [BUILDING NAME] [PATH TO DATA FILE]
#
# Data file in the format: 
# DATE (2014-Jan-01 HH:MM:SS.000),DEMAND (XX.XXX),NET (XX.XXX)
##

database_name = "capstone"

def checkBuildingId(c, building):
    # See if building is already in database
    rows = c.execute("SELECT bid FROM buildings WHERE name=%s", (building,));

    if rows > 0:
        return c.fetchone()[0]
    else:
        return -1


# Check if building is already in database and get its id
# Otherwise create a new entry
def getBuildingId(c, building):
    bid = checkBuildingId(c, building)
    if bid == -1:
        c.execute("INSERT INTO buildings (name) VALUES (%s)", (building,));

    return checkBuildingId(c, building)
        

# Load data from CSV file
def getDataFromFile(bid, filename):
    data = []

    f = open(filename, 'r')
    # Skip first row (header)
    lines = iter(f)
    next(lines)
    for line in lines:
        # Split CSV
        # DATE (2014-Jan-01 HH:MM:SS.000),DEMAND (XX.XXX),NET (XX.XXX)
        time, demand, net = line.strip().split(",")

        # Convert time to datetime object
        time = parse(time)
        #time = datetime.datetime.strptime(time, "%Y-%b-%d %H:%M:%S.%f")
        #time = datetime.datetime.strftime(time, "%Y-%m-%d %H:%M:%S")

        data.append((bid, time, demand, net))

    return data

# Populate!
def populate(building, data_file):
    # Connect to DB
    db = database.connect(database_name)
    c = db.cursor()

    # Main
    bid = getBuildingId(c, building);
    data = getDataFromFile(bid, data_file)

    n = 0
    skippedlines = 0
    # Insert each line into the database
    for line in data:
        try:
            n += c.execute("INSERT INTO energy_data (bid, timestamp, demand, net) VALUES (%s, %s, %s, %s)", line)
        except Exception, msg:
            skippedlines += 1

    db.commit()
    print "Added %s: %s" % (building, data_file)
    print "Added %s rows" % n
    print "Skipped %s lines" % (skippedlines)
    


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "Incorrect usage: python populate.py [ buildingname ] [ data_file | directory ]"
    else:
        # Get program arguments: populate.py building datafile
        building = sys.argv[1]
        data_file = sys.argv[2]

        # data_file may be a directory. Is so, populate recursively
        if os.path.isdir(data_file):
            for root, subdir, files in os.walk(data_file):
                for f in files:
                    # We only care about csv files
                    if f.split(".")[-1] == "csv":
                        data_file = os.path.join(root, f)
                        populate(building, data_file)
        else:
            populate(building, data_file)
