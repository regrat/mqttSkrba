#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  based on version created by MJRoBot.org 
# https://www.hackster.io/mjrobot/from-data-to-graph-a-web-journey-with-flask-and-sqlite-4dba35
#
# pip3 install --upgrade Flask
#

'''
    RPi WEb Server for DHT captured data with Gage and Graph plot
'''

from datetime import datetime

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io, sys, json

from flask import Flask, render_template, send_file, make_response, request
from flask import send_file, send_from_directory, safe_join, abort

from flask import g, redirect, render_template, url_for, jsonify

import os, socket
import meritve as M

app = Flask(__name__)

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

import sqlite3

mydb = '/home/pi/mqttSkrba/sensorsData.db'
meritve = M.Meritve(socket.gethostname())

def debug(s):
    if False:
        print(s,file=sys.stdout)

# Retrieve LAST data from database
def getLastData():
    meritve.reset()
    oneRowOfData = {}
    conn=sqlite3.connect(mydb)
    curs=conn.cursor()
    for row in meritve.cursExecuteSelect(curs, 1):
        oneRowOfData = meritve.setRow(row)
    conn.close()
    return oneRowOfData


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def getDataJSON (numOfAllSamples):
    conn=sqlite3.connect(mydb)
    conn.row_factory = dict_factory
    curs=conn.cursor()
    meritve.cursExecuteSelect(curs, numOfAllSamples)
    data = curs.fetchall()
    conn.close()
    return json.dumps(data)


# Get Max number of rows (table size)
def maxRowsTable():
    conn=sqlite3.connect(mydb)
    curs=conn.cursor()
    for row in curs.execute("select COUNT(client_001) from T_data"):
        maxNumberRows=row[0]
    conn.close()
    return maxNumberRows


# define and initialize global variables
global numOfAllSamples
numOfAllSamples = maxRowsTable()
debug('GLOBAL numOfAllSamples: ' + str(numOfAllSamples))

global rangeTime
rangeTime = 1


# main route 
@app.route("/")
def index():
    oneRowOfData = getLastData()

    #print('This is error output', file=sys.stderr)
    debug('DEBUG: app.route')
    debug('DEBUG: one row = ' + str(oneRowOfData))
    return render_template('index.html', value=oneRowOfData)


@app.route('/', methods=['POST'])
def my_form_post():
    global numOfAllSamples
    global rangeTime
    debug('DEBUG: /')
    rangeTime = int (request.form['n'])

    debug('This is POST')
    return render_template('show.html', n=rangeTime)


@app.route('/show.html', methods=['GET', 'POST'])
def people():
    debug('DEBUG: /show.html - temperatures, calling show.html')
    return render_template('show.html')


@app.route("/v3/getTEST/<csv_id>")
def getTEST(csv_id):
    debug('DEBUG: /v3/getTEST/<csv_id>')
    app.config["CLIENT_CSV"] = "/home/pi/mqttSkrba/srvWebMqtt/templates/v3"
    filename = f"{csv_id}.json"

    try:
        return send_from_directory(app.config["CLIENT_CSV"], filename=filename, as_attachment=True)
    except FileNotFoundError:
        abort(404)


@app.route("/test.html")
def test():
    debug('test')
    return render_template('test.html')


@app.route("/get/<json_id>")
def get(json_id):
    global numOfAllSamples
    global rangeTime

    debug('DEBUG: /get/<json_id>')
    debug('       json_id='+json_id)
    rangeTime = int(request.args.get('n'))

    debug('GLOBAL numOfAllSamples: '+str(numOfAllSamples))
    debug('GLOBAL n: '+str(rangeTime))

    datajson = getDataJSON(rangeTime)

    json_object = json.loads(datajson)

    x = json.dumps(json_object)
    debug('DEBUG JSON='+x)
    return x


if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=False)

