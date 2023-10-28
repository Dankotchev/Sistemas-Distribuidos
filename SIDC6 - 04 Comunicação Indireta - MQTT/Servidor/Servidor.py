import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado ao broker MQTT.")
    else:
        print("Falha na conexão com o broker MQTT.")

def on_message(client, userdata, msg):
    temperatura = 0

    if msg.topic == "controle/maquina":
        if msg.payload.decode() == "AUMENTAR":
            print("CONTROLE: AUMENTAR TEMPERATURA")
        elif msg.payload.decode() == "DIMINUIR":
            print("CONTROLE: DIMINUIR TEMPERATURA")
    elif msg.topic == "temperatura/maquina":
        temperatura = int(msg.payload)
        if temperatura > 125:
            print("TEMPERATURA: ACIMA DO LIMITE")
        elif temperatura < 60:
            print("TEMPERATURA: ABAIXO DO LIMITE")
        else:
            print("TEMPERATURA: NO LIMITE")

broker_address = "localhost"
port = 1883

client = mqtt.Client("ServidorMQTT")
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_address, port, 60)
client.subscribe("controle/maquina")
client.subscribe("temperatura/maquina")

client.loop_forever()
