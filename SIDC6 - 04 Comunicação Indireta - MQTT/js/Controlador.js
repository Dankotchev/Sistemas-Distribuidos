const mqtt = require('mqtt');
const brokerUrl = 'mqtt://localhost:1883';

const client = mqtt.connect(brokerUrl, { clientId: 'CentralControle' });

client.on('connect', () => {
  console.log('Conectado ao broker MQTT.');
  client.subscribe('temperatura/maquina');
});

client.on('message', (topic, message) => {
  const temperatura = parseInt(message.toString());

  if (temperatura > 125) {
    console.log(`Alerta: Sobreaquecimento detectado! Temperatura: ${temperatura}`);
    client.publish('controle/maquina', 'DIMINUIR');
  } else if (temperatura < 60) {
    console.log(`Alerta: Baixa temperatura detectada! Temperatura: ${temperatura}`);
    client.publish('controle/maquina', 'AUMENTAR');
  } else {
    console.log(`Temperatura normal: ${temperatura}`);
  }
});

client.on('error', (error) => {
  console.error('Falha na conexão com o broker MQTT:', error);
});
