import paho.mqtt.client as mqtt
import time
import random

broker_address = "localhost"
port = 1883


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado ao broker MQTT.")
        client.publish("temperatura/maquina", payload="70", qos=0, retain=False)
    else:
        print("Falha na conexão com o broker MQTT.")

def on_message(client, userdata, msg):
    if msg.topic == "controle/maquina":
        if msg.payload.decode() == "AUMENTAR":
            temperatura = random.randint(60, 75)
        elif msg.payload.decode() == "DIMINUIR":
            temperatura = random.randint(100, 120)
        client.publish("temperatura/maquina", payload=str(temperatura), qos=0, retain=False)

client = mqtt.Client("MaquinarioMQTT")
client.on_connect = on_connect
client.on_message = on_message
temperatura = 70

client.connect(broker_address, port, 60)

while True:
    temperatura += random.randint(-15, 15)
    client.publish("temperatura/maquina", payload=str(temperatura), qos=0, retain=False)
    time.sleep(random.uniform(0.5, 1))

client.loop_forever()
