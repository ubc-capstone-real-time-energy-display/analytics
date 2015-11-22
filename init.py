import os
import sys
import analytics.util.populate as populate
import analytics.util.database as database

##
# Run this file to seed the database with all the data files 
# USAGE: python init.py
##

data_root = "analytics/data"
structure_file = "analytics/database/structure_only.sql"

# Create the database
def createdatabase():
    db = database.connect()
    c = db.cursor()

    f = open(structure_file, "r")
    sqlfile = f.read()
    f.close()

    sqlcommands = sqlfile.split(";")

    print "Creating database"
    for command in sqlcommands:
        try:
            c.execute(command)
            db.commit()
        except Exception, msg:
            print "Command skipped: ", msg

    db.close()
    print "Created database"


# Seed
def seed():
    print "Seeding database"
    for root, subdir, files in os.walk(data_root):
        buildingname = root.split("/")[-1]

        for f in files:
            # We only care about csv files
            if f.split(".")[-1] == "csv":
                data_file = os.path.join(root, f)
                populate.populate(buildingname, data_file)

    print "Seeded database"

createdatabase()
seed()

