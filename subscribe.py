import paho.mqtt.client as mqtt
import threading

#inisiasi
broker_port = 1883
broker_addr = "192.168.1.15"

#inisiasi list
clients = []
threads = []

class pubThread(threading.Thread):
    def __init__(self, threadID, name, client):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.client = client
    def run(self):
        print("Start..."+self.name)
        mainSubscribe(self.client,broker_addr)
        print("Selesai..."+self.name)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connection successful")
    else :
        print("Connection refused")

def on_message(client, userdata, message):
    print("topic received.. ",message.topic)
    print("message received.. "+str(message.payload))
    #print("qos received.., ",message.qos)

def mainSubscribe(client, addr):
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(addr,broker_port,)
    client.subscribe("home")
    client.loop_forever()

for i in range(0,10):
    clients.append(mqtt.Client("Subscribe "+str(i)))

for i in range(len(clients)):
    threads.append(pubThread(1,"Thread ke-"+str(i), clients[i]))

for i in range(len(clients)):
    threads[i].start()

for i in range(len(clients)):
    threads[i].join()
