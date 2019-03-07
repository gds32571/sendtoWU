#!/usr/local/bin/python3

# program to send data to WU
# 2 Mar 2019 gswann

# https://feedback.weather.com/customer/en/portal/articles/2924682-pws-upload-protocol?b_id=17298

import pdb

from datetime import datetime
import time

from time import sleep

import json

#import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt

from subprocess import Popen, PIPE

global myAtemp 
global myAhumi
global myAwind
global myAwinddir
global myAlanai
global myAlhumi

global oldmin

global time1
global time2
global time3
global time4

time1 = time.time()
time2 = time.time()
time3 = time.time()
#time4 = time.time()

# originally, this was HA "retransmits" of the values (not JSON)
# now - is the original rtl transmissions
myTopic1 = "rtl433/acurite/cha"
myTopic2 = "rtl433/acurite/wind"
myTopic3 = "rtl433/acurite/lanai"
#myTopic4 = "rtl433/acurite/wind"

oldmin = datetime.now().minute - 1
now = datetime.now()
# print(str(now))

myTime = (now.strftime("%A %Y/%m/%d %H:%M"))
print(myTime)

myAtemp = "un"
myAhumi = "un"
myAwind = "un"
myAwinddir = "un"
myAlanai = "un"
myAlhumi = "un"

################################################
def on_connect(client, userdata, rc, flags):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.

    client.subscribe(myTopic1)
    print ("Subscribing to " + myTopic1)

    client.subscribe(myTopic2)
    print ("Subscribing to " + myTopic2)

    client.subscribe(myTopic3)
    print ("Subscribing to " + myTopic3)

#    client.subscribe(myTopic4)
#    print ("Subscribing to " + myTopic4)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global myAtemp
    global myAhumi
    global myAwind
    global myAwinddir
    global myAlanai
    global myAlhumi
    
    global time1
    global time2
    global time3

    global oldmin
    
#    pdb.set_trace()

    print('\033[33m',end='')
#    print(msg.topic+" "+str(msg.payload))
    print(msg.topic,end='  ')
    print('\033[0m',end='')
    myPayload = msg.payload.decode('utf-8')
    decoded = json.loads(myPayload)
    
    try:

        if (msg.topic == myTopic1):
           print('\a',end='')
           print('\033[33m'+str(msg.payload)+'\033[0m')
           print ("Time: ",end='  ')
           print (decoded['time'],end='  ')
           print (decoded['temperature_F'])

#           myAtemp = round(((decoded['temperature_C']) * 9 /5)+32,1)
           myAtemp = decoded['temperature_F']
           myAhumi = decoded['humidity']
           myAwind = round(decoded['wind_speed_kph'] * 0.62137,1)
           time1 = time.time() 
#           print (myAtemp)

        if (msg.topic == myTopic2):
           print('\a',end='')
           print('\033[34m'+str(msg.payload)+'\033[0m')
           print ("Time: ",end='  ')
           print (decoded['wind_speed_kph'],end='  ')
           print (decoded['wind_dir_deg'])

           myAwind = round(decoded['wind_speed_kph'] * 0.62137,1)
           myAwinddir = decoded['wind_dir_deg']
           time2 = time.time() 

        if (msg.topic == myTopic3):
#           print('\a',end='')
           print('\033[35m'+str(msg.payload)+'\033[0m')
           print ("Time: ",end='  ')
           print (decoded['time'],end='  ')
           print (decoded['temperature_C'])

           myAlanai = round(((decoded['temperature_C']) * 9 /5)+32,1)
           myAlhumi = decoded['humidity']
           time3 = time.time() 
    except:
        print("error encountered")
   
    
    oldmin = datetime.now().minute - 1

######################################
client = mqtt.Client()
client.username_pw_set('hass', password='hass')
client.on_connect = on_connect
client.on_message = on_message
client.connect_async("ha32163", 1883, 60)


client.loop_start()

print('\033[34m',end='')
p = Popen(["./socket1.py", "3005" ])
print('\033[0m',end='')

######################################
while(True):
#    global oldmin
    while oldmin == datetime.now().minute:
        sleep(1)

    if (datetime.now().second == 0):
     #if (myAtemp == "un" and myAlanai != "un"):
         #myAtemp = str(round(float(myAlanai) - 7.0,1))
         #if (myAhumi == "un"):
          #  myAhumi = myAlhumi

     #if (myAtemp != "un" and myAhumi != "un"):
      print(" ")
      p = Popen(["./wu_post-v2.pl"], stdin = PIPE, stdout=PIPE)
      p.stdin.write(str(myAtemp).encode())
      p.stdin.write(b'\n')

      p.stdin.write(str(myAhumi).encode())
      p.stdin.write(b'\n')
      p.stdin.write(str(myAwind).encode())
      p.stdin.write(b'\n')
      p.stdin.write(str(myAwinddir).encode())
      p.stdin.write(b'\n')

      p.stdin.write(str(myAlanai).encode())
      p.stdin.write(b'\n')

      p.stdin.close()
      print ('WU updated')

      print('\033[34m',end='')
      p = Popen(["./socket1.py", "3005" ])
      print('\033[0m',end='')

    oldmin = datetime.now().minute

    now = datetime.now()

    #pdb.set_trace()


    myTime = (now.strftime("%A %b %-d  %H:%M"))

    myMessage = myTime  
    myMessage = myMessage + "  local:" +  str(myAtemp) + "  humi:" \
        +  str(myAhumi) + " wind:" + str(myAwind) \
        + " direction:" + str(myAwinddir) \
        + " lanai:" + str(myAlanai)
    
    print (myMessage)

    print(f'Timer values       \033[31m      {(time.time() - time1):3.2f}             {(time.time() - time2):3.2f}                  {(time.time() - time3):3.2f} \033[0m')

    if time.time() - time1  > 360:
        myAtemp = "un"
        myAhumi = "un"
        print("data timeout 1")

    if time.time() - time2  > 360:
        myAwind = "un"
        myAwinddir = "un"
        print("data timeout 2")

    if time.time() - time3  > 90:
        myAlanai = "un"
        print("data timeout 3")


