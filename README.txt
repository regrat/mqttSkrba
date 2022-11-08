vi /etc/rc.local

/usr/bin/python3 /home/pi/tipke.py  > /dev/null 2>&1 &
/usr/bin/python3 /home/pi/mqtt/mqttSrv.py   > /home/pi/mqtt/logs/mqttSrv.log 2>&1  &
/usr/bin/python3 /home/pi/mqtt/srvWebMqtt/appjson_v3.py & > /home/pi/mqtt/logs/appjson_v3.log 2>&1


http://192.168.0.28/show.html?&num=245

