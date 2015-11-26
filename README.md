# About

This code is for getting a rough idea of how much energy is used at UBC. This project relies on a database populated with building consumption data.

# Setup

## Python

This project is written in Python 2. 

It depends on:

1. matplotlib
2. MySQLdb

Use pip to install the dependencies.

## Database

1. Create a new user (see util/database.py for credentials)
2. Run `python init.py` to create and seed the database

# Usage

## New Data
Use this command to insert new data (after seeding) into the database

```
python populate.py [building name] [csv file path]
```

## Overview
Use `python overview.py [building name]` to see the all the data available for the building

## Metrics
Try different metrics using:

```
python visualize.py [metric] [buildingname] [date (YYYY-MM-DD)]
```
