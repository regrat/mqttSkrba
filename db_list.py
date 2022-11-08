#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#  insertDataTableDHT.py
#  
#  Developed by Marcelo Rovai, MJRoBot.org @ 9Jan18
#  
#  Query dada on table "DHT_data" 

import sqlite3

conn=sqlite3.connect('sensorsData.db')

curs=conn.cursor()

print ("\nEntire database contents:\n")
for row in curs.execute("SELECT * FROM T_data"):
    print (row)

print("All records:")
for row in curs.execute("SELECT COUNT(timestamp) from T_data"):
    print (row)
    print (row[0])
conn.close()
