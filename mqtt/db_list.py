#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#  show data in the database


import sqlite3

conn=sqlite3.connect('sensorsData.db')

curs=conn.cursor()

print ("\nEntire database contents:\n")
for row in curs.execute("SELECT * FROM T_data"):
    print (row)

print("Number of records:")
for row in curs.execute("SELECT COUNT(timestamp) from T_data"):
    print (row)
    print (row[0])
conn.close()
