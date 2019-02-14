#import library paho
import paho.mqtt.client as mqtt
import json
import random
import threading
import time

#inisiasi client
broker_port = 1883
broker_addr = "192.168.1.15"

#inisiasi list
clients =[]
threads =[]

#inisiasi payload
randNumber = random.randint(0,200)
topic = "home"
mqttPayload= json.dumps({
    "temp" : randNumber,
    "hum" : randNumber,
    "Tv" : "OFF",
    "Ac" : "On",
    "door" : "Locked",
    "light" : "ON",
    "msg" : "Here your message"
})

class pubThread(threading.Thread):
    def __init__(self, threadID, name, client):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.client = client
    def run(self):
        print("Start "+self.name)
        mainPublish(self.client,broker_addr)
        print("Selesai..."+self.name)

#callback publish
def on_publish(client, userdata, mid):
    print("Data published...")

def on_disconnect(client, userdata, rc):
    print("Client disconnected...")

#callback koneksi
def on_connect(client, userData, flags, rc):
    if rc == 0:
        print("Connection successful ")
    else :
        print("Connection refused, return code= ",rc)

#untuk qos
def on_log(client, userdata, level, buff):
    print("log: ",buff)

def mainPublish(client, addr):
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.connect(addr,broker_port)
    client.loop_start()
    client.publish(topic,mqttPayload)
    time.sleep(1)
    client.on_disconnect = on_disconnect
    client.disconnect()
    client.loop_stop()

for i in range(0,20):
    clients.append(mqtt.Client("Publish: "+str(i)))

print("Thread")

for i in range(len(clients)):
    threads.append(pubThread(1, "Thread ke-"+str(i), clients[i]))

for i in range(len(clients)):
    threads[i].start()

for i in range(len(clients)):
    threads[i].join()

print("Thread Selesai")