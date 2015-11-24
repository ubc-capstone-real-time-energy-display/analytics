import database

databasename = "capstone"

def _getcursor(databasename):
    db = database.connect(databasename)
    return db.cursor()


def getbid(buildingname):
    c = _getcursor(databasename)
    c.execute("SELECT bid FROM buildings WHERE name=%s", (buildingname,))

    bid = c.fetchone()[0]
    c.close()

    return bid

"""
Get energy usage data for the given building between two dates

@param bid  int
@param dateStart  string (YYYY-MM-DD)
@param dateStop  string (YYYY-MM-DD)
"""
def getdata(bid, dateStart, dateStop):
    c = _getcursor(databasename)
    c.execute("SELECT timestamp, demand FROM energy_data WHERE (timestamp BETWEEN %s AND %s) AND bid=%s", (dateStart, dateStop, bid))

    data = c.fetchall()
    c.close()

    return data
