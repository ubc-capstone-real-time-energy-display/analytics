import sys
import datetime 
import database

##
# USAGE:  python populate.py [BUILDING NAME] [PATH TO DATA FILE]
#
# Data file in the format: 
# DATE (2014-Jan-01 HH:MM:SS.000),DEMAND (XX.XXX),NET (XX.XXX)
##

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
        time = datetime.datetime.strptime(time, "%Y-%b-%d %H:%M:%S.%f")
        time = datetime.datetime.strftime(time, "%Y-%m-%d %H:%M:%S")

        data.append((bid, time, demand, net))

    return data



# Get program arguments: populate.py building datafile
building = sys.argv[1]
data_file = sys.argv[2]

# Connect to DB
db = database.connect()
c = db.cursor()

# Main
bid = getBuildingId(c, building);
data = getDataFromFile(bid, data_file)

n = 0
# Insert each line into the database
for line in data:
    n += c.execute("INSERT INTO energy_data (bid, timestamp, demand, net) VALUES (%s, %s, %s, %s)", line)

print n
db.commit()
