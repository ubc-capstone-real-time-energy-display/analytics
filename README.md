# About

This code is for getting a rough idea of how much energy is used at UBC. This project relies on a database populated with building consumption data.

# Setup

This project is written in Python 2. 

It depends on:

1. matplotlib
2. MySQLdb

# Usage

Use this command to insert data into the database

```
python populate.py [building name] [csv file path]
```

Modify analyze.py to run queries
```
python analyze.py
```
