#!/usr/bin/python3
# See also:
#   https://github.com/eclipse/paho.mqtt.python
#
# Installation and start
"""
  sudo apt-get install -y sshfs
  sudo apt-get install python3-pip
  sudo apt-get install python3-dev python3-rpi.gpio
  sudo apt-get install sqlite3
  sudo apt-get install mosquitto
  sudo pip3 install paho-mqtt
  sudo pip3 install beautifulsoup4
  sudo apt-get install python3-flask
  sudo apt-get install python3-matplotlib

  sudo vi /etc/rc.local
  /usr/bin/python3 /home/pi/mqttSkrba/mqttSrv.py   > /home/pi/mqttSkrba/logs/mqttSrv.log 2>&1  &
"""

import paho.mqtt.client as mqtt
import sqlite3
import time, sys

import readTemp as B18
import readLJ as LJ
import srvWebMqtt.meritve as M
import socket

dbname = '/home/pi/mqttSkrba/sensorsData.db'

broker_url = "127.0.0.1"
broker_port = 1883

meritve = M.Meritve(socket.gethostname())
if len(sys.argv) > 1:
    dbg = True
else:
    dbg = False

def debug(s):
    global dbg
    if dbg:
        print(s)

def on_connect(client, userdata, flags, rc):
    global loop_flag
    print("Connected With Result Code " +str(rc))
    if rc != 0:
        print("0: Connection successful 1: Connection refused – incorrect protocol version 2: Connection refused – invalid client identifier")
        print("3: Connection refused – server unavailable 4: Connection refused – bad username or password 5: Connection refused.")
        loop_flag = 0

def on_disconnect(client, userdata, rc):
    print("Client Got Disconnected")

def on_message_from_CLIENT_001(client, userdata, message):
    debug("Message received CLIENT_001 = "+message.payload.decode())
    meritve.set("client_001", float(message.payload.decode()))

def on_message_from_CLIENT_002(client, userdata, message):
    debug("Message received CLIENT_002 = "+message.payload.decode())
    meritve.set("client_002", float(message.payload.decode()))

def on_message_from_CLIENT_003(client, userdata, message):
    debug("Message received CLIENT_003 = "+message.payload.decode())
    meritve.set("client_003", float(message.payload.decode()))

def on_message(client, userdata, message):
    debug("UKNOWN message received "+message.topic+" = "+message.payload.decode())

def add_data_to_DB ():
    debug(time.strftime("%Y-%b-%d %H:%M:%S", time.localtime())+": DB update...")
    conn=sqlite3.connect(dbname)
    curs=conn.cursor()
    meritve.cursExecuteInsert(curs)
    conn.commit()
    conn.close()
    #meritve.printAll()


def one_loop():
    meritve.reset()

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    #To Process Every Other Message
    client.on_message = on_message

    print("Connecting...")
    client.connect(broker_url, broker_port)

    print("Subscribing...")
    client.subscribe([("TestingTopic", 1),
                    ("CLIENT_001",     1),
                    ("CLIENT_001DEBUG",1),
                    ("CLIENT_002",     1),
                    ("CLIENT_002DEBUG",1),
                    ("CLIENT_003",      1),
                    ("CLIENT_003DEBUG", 1)
                    ])
    print("Adding callback...")
    client.message_callback_add("CLIENT_001", on_message_from_CLIENT_001)
    client.message_callback_add("CLIENT_002", on_message_from_CLIENT_002)
    client.message_callback_add("CLIENT_003", on_message_from_CLIENT_003)

    print("Starting loop...")
    loop_flag = 1
    #client.loop_forever()
    client.loop_start()

    while loop_flag ==1:

        debug("Sending trigger...")
        client.publish("TRIGGER","ON")
        time.sleep(2)   #wait to collect all mqtt client data
        debug("Checking ARSO...")

        lj = LJ.getTemp()
        debug("DEBUG: LJ: " + lj)
        meritve.set("lj", lj)

        piTemp = B18.read_temp()
        debug("B18 konec...")
        if len(piTemp) > 0:
            dnevnaSoba = piTemp[0]
            if isinstance(dnevnaSoba, float):
                meritve.set("RPI", dnevnaSoba)
            if len(piTemp) > 1:
                radiator = piTemp[1]
                if isinstance(radiator, float):
                    meritve.set("RPIa", radiator)
        else:
            debug("No RPI temperatures available")

        add_data_to_DB ()
        meritve.reset()
        time.sleep(20*60)  #every 20 minutes
        #time.sleep(10)  #every 15s

    client.disconnect()
    print("client loop stopped")
    client.loop_stop()

while True:
    one_loop()
