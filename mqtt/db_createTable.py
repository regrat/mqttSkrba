#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#  create empty database

import sqlite3 as lite
import sys
import socket

from pathlib import Path
script_dir = Path(__file__).resolve().parent
target_dir = str(script_dir.parent / "srvWebMqtt")
sys.path.append(target_dir)
import meritve as M

con = lite.connect('../sensorsData.db')

# add_data (0.0, 0.0, 0.0)

m  = M.Meritve(socket.gethostname())

with con:
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS T_data")
    m.curExecuteCreate(cur)

