#include "mosquitto.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct mosquitto *mosq;

void on_connect(struct mosquitto *mosq, void *userdata, int rc) {
    if (rc == 0) {
        printf("Conectado ao broker MQTT.\n");
    } else {
        printf("Falha na conexão com o broker MQTT.\n");
    }
}

void on_message(struct mosquitto *mosq, void *userdata, const struct mosquitto_message *message) {
     // Processar mensagens recebidas, se necessário
	int temperatura;

	 if (strncmp(message->topic, "controle/maquina", message->topic_len) == 0) {
        if (strncmp(message->payload, "AUMENTAR", message->payloadlen) == 0)
            printf("CONTROLE: AUMENTAR TEMPERATURA\n");
        else if (strncmp(message->payload, "DIMINUIR", message->payloadlen) == 0)
            printf("CONTROLE: DIMINUIR TEMPERATURA\n");

    } else if (strncmp(message->topic, "temperatura/maquina", message->topic_len) == 0)	{
		temperatura = atoi((char *)message->payload);
		if (temperatura > 125){
			printf("TEMPERATURA: ACIMA DO LIMITE\n");
		else if (temperatura < 60){
			printf("TEMPERATURA: ABAIXO DO LIMITE\n");
		else
			printf("TEMPERATURA: NO LIMITE\n");
	}
}

int main() {
    mosquitto_lib_init();

    mosq = mosquitto_new("ServidorMQTT", true, NULL);
    mosquitto_connect_callback_set(mosq, on_connect);
    mosquitto_message_callback_set(mosq, on_message);

    if (mosquitto_connect(mosq, "localhost", 1883, 60) != MOSQ_ERR_SUCCESS) {
        fprintf(stderr, "Não foi possível conectar ao broker MQTT.\n");
        return 1;
    }

    mosquitto_loop_forever(mosq, -1, 1);

    mosquitto_destroy(mosq);
    mosquitto_lib_cleanup();

    return 0;
}
