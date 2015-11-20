import sys
import MySQLdb as mysql

# Database information
host = "127.0.0.1"
port = 8889
username = "capstone"
password = "abc123"
database = "capstone"

# Connect to the database
# Returns: Database object
def connect():
    db = mysql.connect(host=host, port=port, user=username, passwd=password, db=database)
    return db
