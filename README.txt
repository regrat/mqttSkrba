/etc/rc.local:
  #verify: sudo /etc/init.d/rc.local start
  /usr/bin/python3 /home/pi/tipke.py  > /dev/null 2>&1 &
  /usr/bin/python3 /home/pi/mqttSkrba/mqttSrv.py             > /home/pi/mqttSkrba/logs/mqttSrv.log 2>&1  &
  /usr/bin/python3 /home/pi/mqttSkrba/srvWebMqtt/appjson.py 2> /home/pi/mqttSkrba/logs/appjson.log 1>/dev/null &

/etc/mosquitto/mosquitto.conf:
  log_timestamp_format %Y-%m-%dT%H:%M:%S
  listener 1883
  allow_anonymous true
