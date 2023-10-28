import paho.mqtt.client as mqtt

broker_address = "localhost"
port = 1883

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado ao broker MQTT.")
        client.subscribe("temperatura/maquina")
    else:
        print("Falha na conexão com o broker MQTT.")

def on_message(client, userdata, msg):
    temperatura = int(msg.payload)
    if temperatura > 125:
        print(f"Alerta: Sobreaquecimento detectado! Temperatura: {temperatura}")
        client.publish("controle/maquina", payload="DIMINUIR", qos=0, retain=False)
    elif temperatura < 60:
        print(f"Alerta: Baixa temperatura detectada! Temperatura: {temperatura}")
        client.publish("controle/maquina", payload="AUMENTAR", qos=0, retain=False)
    else:
        print(f"Temperatura normal: {temperatura}")

client = mqtt.Client("CentralControle")
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_address, port, 60)

client.loop_forever()
