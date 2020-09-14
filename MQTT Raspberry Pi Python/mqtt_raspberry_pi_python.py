# Install MQTT Client
# sudo apt update
# sudo apt upgrade
# sudo apt-get install mosquitto mosquitto-clients
# mosquitto_sub -h localhost -t “test”
# mosquitto_pub -h localhost -t “test” -m “Hello”

# using python MQTT library
# pip install paho-mqtt

import paho.mqtt.client as mqtt
import json
import subprocess
import time
import datetime

MQTT_MSG = []

# Define on_publish event function
def on_connect(client, userdata, flags, rc):
    client.subscribe("RASP_LED_PI") # Subscribe to the topic
    print("Connected with result code "+str(rc))

def on_message(client, userdata, message):
    topic = str(message.topic)
    message = str(message.payload.decode("utf-8"))
    print(topic + '->' + message)

def on_publish(client, userdata, mid):
    print "Message Published..."

# Define MQTT client
client = mqtt.Client("raspPi")
client.on_message = on_message # Attach the on_message function
client.on_connect = on_connect # Attach the on_connect function
client.on_publish = on_publish # Attach the on_publish function
client.loop_start() # Start the MQTT client service
client.connect("localhost", 1883, 60)

def pi_stats():
    global MQTT_MSG
    # Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
    cmd = "hostname -I | cut -d\' \' -f1"
    IP = subprocess.check_output(cmd, shell = True )
    cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
    CPU = subprocess.check_output(cmd, shell = True )
    cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
    MemUsage = subprocess.check_output(cmd, shell = True )
    cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
    Disk = subprocess.check_output(cmd, shell = True )
    x = datetime.datetime.now()
    MQTT_MSG = json.dumps({"IP": str(IP), "CPU": str(CPU), "MemUsage": str(MemUsage), "Disk": str(Disk), "Time": str(x)});

while(1):
    pi_stats()
    client.publish("RASP_SYS_MON", MQTT_MSG) # Publish message to MQTT broker
    time.sleep(3) # Sleep for a second

