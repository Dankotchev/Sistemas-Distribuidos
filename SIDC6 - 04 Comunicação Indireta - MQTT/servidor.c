#include <mosquitto.h>
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
