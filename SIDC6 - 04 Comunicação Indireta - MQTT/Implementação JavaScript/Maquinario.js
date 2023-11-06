const mqtt = require('mqtt');

const brokerUrl = 'mqtt://localhost:1883';

const client = mqtt.connect(brokerUrl, { clientId: 'MaquinarioMQTT' });

let temperatura = 70;

client.on('connect', () => {
  console.log('Conectado ao broker MQTT.');
  client.publish('temperatura/maquina', temperatura.toString());
  client.subscribe('controle/maquina');
});

client.on('message', (topic, message) => {
  if (topic === 'controle/maquina') {
    if (message.toString() === 'AUMENTAR') {
      temperatura = Math.min(temperatura + Math.floor(Math.random() * 16), 100);
			console.log(`Comando: AUMENTAR; Temperatura: ${temperatura}`);
    } else if (message.toString() === 'DIMINUIR') {
      temperatura = Math.max(temperatura - Math.floor(Math.random() * 16), 0);
			console.log(`Comando: DIMINUIR; Temperatura: ${temperatura}`);
    }
    client.publish('temperatura/maquina', temperatura.toString());
  }
});

setInterval(() => {
  temperatura += Math.floor(Math.random() * 31) - 15;
  client.publish('temperatura/maquina', temperatura.toString());
}, Math.random() * 500 + 500);
