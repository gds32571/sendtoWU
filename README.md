# sendtoWU

A pair of programs to collect data from an MQTT server and upload them to Weather Underground.

One of the Raspberry Pi computers here runs a program to read acurite weather data from 
an RTL-SDR radio dongle. The data is transmitted as JSON formatted data which is used by 
Home Assistant to display weather related information collected from the local sensors. Most,
but not all, of the sensors are maintained by me.
 
The first program, sendtoWU-v2.py, is written in Python. It subscribes to weather MQTT publications, extracts the pertinent
values, keeps track of the "freshness" of the data and uploads good data to the Weather Underground
website.
   
A second program, wu_post-v2.pl is a Perl prorgam I wrote several years ago to run on a Linux 
machine. It read data from a file on disk as a source of data.  I modified it to take input from STDIN 
which is then assembled into a GET string and sent to Weather Underground.

The secrets.txt contains the authentication data for WU.  Put your own information in this file.
   
   
