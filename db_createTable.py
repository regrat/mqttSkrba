#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#  createTableDHT.py
#  
# Developed by Marcelo Rovai, MJRoBot.org @ 9Jan18
#  
# Create a table "DHT_data" to store DHT temp and hum data

import sqlite3 as lite
import sys
import socket
import srvWebMqtt.meritve as M

con = lite.connect('sensorsData.db')

# add_data (0.0, 0.0, 0.0)

m  = M.Meritve(socket.gethostname())

with con:
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS T_data")
    m.curExecuteCreate(cur)

