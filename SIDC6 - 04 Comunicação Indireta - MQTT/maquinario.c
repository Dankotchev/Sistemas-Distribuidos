#include "mosquitto.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

struct mosquitto *mosq;
int temperatura = 100;  // Temperatura inicial


void on_connect(struct mosquitto *mosq, void *userdata, int rc) {
    if (rc == 0) {
        printf("Conectado ao broker MQTT.\n");
        // Publica a temperatura inicial no tópico
        char temperatura_str[5];
        sprintf(temperatura_str, "%d", temperatura);
        mosquitto_publish(mosq, NULL, "temperatura/maquina", strlen(temperatura_str), temperatura_str, 0, false);
    } else {
        printf("Falha na conexão com o broker MQTT.\n");
    }
}

void on_message(struct mosquitto *mosq, void *userdata, const struct mosquitto_message *message) {
    if (strncmp(message->topic, "controle/maquina", message->topic_len) == 0) {
        if (strncmp(message->payload, "AUMENTAR", message->payloadlen) == 0)
            temperatura += rand() % 26 - 10;
        else if (strncmp(message->payload, "DIMINUIR", message->payloadlen) == 0)
            temperatura -= rand() % 26 - 10;
    }
}

int main() {
    mosquitto_lib_init();

    mosq = mosquitto_new("MaquinarioMQTT", true, NULL);
    mosquitto_connect_callback_set(mosq, on_connect);
    mosquitto_message_callback_set(mosq, on_message);

    if (mosquitto_connect(mosq, "localhost", 1883, 60) != MOSQ_ERR_SUCCESS) {
        fprintf(stderr, "Não foi possível conectar ao broker MQTT.\n");
        return 1;
    }

    while (1) {
        // Simula o aumento e diminuição da temperatura
		temperatura = rand() % 22 - 10;

        // Publica a temperatura no tópico
        char temperatura_str[5];
        sprintf(temperatura_str, "%d", temperatura);
        mosquitto_publish(mosq, NULL, "temperatura/maquina", strlen(temperatura_str), temperatura_str, 0, false);

        sleep(rand() % 2000 + 500);
    }

    mosquitto_loop_forever(mosq, -1, 1);

    mosquitto_destroy(mosq);
    mosquitto_lib_cleanup();

    return 0;
}
