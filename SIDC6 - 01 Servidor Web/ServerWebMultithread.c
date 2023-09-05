#include <io.h>
#include <stdio.h>
#include <winsock2.h>
#include <string.h>
#include <time.h>

#pragma comment(lib, "ws2_32.lib")

#define PORT 80
#define MESSAGESIZE 255
#define MAXSOCKETS 10

SOCKET new_socket[MAXSOCKETS];
int qtdsockets = 0;

typedef struct
{
	char palavras[3][50];
} Requisicao;

void obterNomePaginaSemBarra(char *nomeArquivo)
{
	for (int i = 0; i < strlen(nomeArquivo); i++)
		nomeArquivo[i] = nomeArquivo[i + 1];
}

char *lerArquivo(const char *nomeArquivo)
{

	FILE *arquivo = fopen(nomeArquivo, "r");
	if (arquivo == NULL)
	{
		fclose(arquivo);
		// return lerArquivo("404.html", codigo);
		return NULL;
	}

	fseek(arquivo, 0, SEEK_END);
	long tamanho = ftell(arquivo);
	fseek(arquivo, 0, SEEK_SET);

	char *conteudo = (char *)malloc(tamanho + 1);

	fread(conteudo, 1, tamanho, arquivo);
	conteudo[tamanho] = '\0';
	fclose(arquivo);
	return conteudo;
}

char *montarPaginaResposta(const char *arquivo)
{
	// Tratamento do arquivo a ser lido
	// codigo de retorno
	int codigo = 200;
	// leitura da página HTML
	char *pagina = lerArquivo(arquivo);
	if (pagina == NULL)
	{
		pagina = lerArquivo("404.html");
		codigo = 404;
	}

	// tamanho da página HTML em int
	int tam = strlen(pagina);
	// tamanho da pagina HTML em char
	char tamChar[MESSAGESIZE];
	// conversão do tamanho de inteiro para char
	itoa(tam, tamChar, 10);

	// Obter a data e hora atual em UTC
	time_t dataSistema;
	struct tm *infoTime;
	time(&dataSistema);
	infoTime = gmtime(&dataSistema);

	// Formatar a data no formato desejado
	char dataFormatada[80];
	strftime(dataFormatada, sizeof(dataFormatada), "Date: %a, %d %b %Y %X %Z", infoTime);

	// Montagem da resposta
	// alocação de tamanho para a página mais os cabeçalhos
	char *resposta = (char *)malloc(tam + 400);

	if (codigo == 200)
		strcpy(resposta, "HTTP/1.1 200 OK\r\n");
	else if (codigo == 404)
		strcpy(resposta, "HTTP/1.1 404 Not Found\r\n");
	strcat(resposta, dataFormatada);
	strcat(resposta, "\r\n");
	strcat(resposta, "Sever: Meu Primeiro Servidor/0.5\r\n");
	strcat(resposta, "Accept-Ranges: bytes\r\n");
	strcat(resposta, "Content-Lenght: ");
	strcat(resposta, tamChar);
	strcat(resposta, "\r\n");
	strcat(resposta, "Content-Type: text/html\r\n\n");
	strcat(resposta, pagina);
	strcat(resposta, "\r\n\n");

	free(pagina);
	return resposta;
}

void processarRequisicao(int pos, Requisicao *req)
{
	char *resposta;

	if (strcmp(req->palavras[0], "GET") == 0)
	{
		if (strcmp(req->palavras[1], "/") == 0)
			resposta = montarPaginaResposta("index.html");
		else
		{
			obterNomePaginaSemBarra(req->palavras[1]);
			resposta = montarPaginaResposta(req->palavras[1]);
		}
		send(new_socket[pos], resposta, strlen(resposta) + 1, 0);
	}
	// printf(resposta);
	// printf("\n\nTamanho resposta: %d", strlen(resposta));
	free(resposta);
	// printf("\n\n\n\t\t\tLiberdade cantou!\n\n");
	// printf(resposta);
	// printf("\n\nTamanho resposta: %d", strlen(resposta));
}

Requisicao tratarChamado(char *mensagem)
{
	Requisicao req;
	char *token;
	int contador = 0;

	token = strtok(mensagem, " ");

	while (token != NULL && contador < 3)
	{
		strcpy(req.palavras[contador], token);
		token = strtok(NULL, " ");
		contador++;
	}
	return req;
}

void tratarConexao(int pos)
{
	char message[MESSAGESIZE];
	Requisicao req;
	int len;

	message[0] = '\0';
	len = recv(new_socket[pos], message, MESSAGESIZE, 0);
	req = tratarChamado(message);

	if (len > 0)
		processarRequisicao(pos, &req);

	//closesocket(new_socket[pos]);
}

int main(int argc, char *argv[])
{
	WSADATA wsa;
	SOCKET s;
	struct sockaddr_in server, client;
	int c, pos;
	char errormessage[MESSAGESIZE];

	printf("*** SERVER ***\n\nAguardando conexoes...\n\n");

	if (WSAStartup(MAKEWORD(2, 2), &wsa) != 0)
	{
		printf("\nFalha na inicializacao da biblioteca Winsock: %d", WSAGetLastError());
		exit(EXIT_FAILURE);
	}

	if ((s = socket(AF_INET, SOCK_STREAM, 0)) == INVALID_SOCKET)
	{
		printf("\nNao e possivel inicializar o socket: %d", WSAGetLastError());
		exit(EXIT_FAILURE);
	}

	server.sin_family = AF_INET;
	server.sin_addr.s_addr = INADDR_ANY;
	server.sin_port = htons(PORT);

	if (bind(s, (struct sockaddr *)&server, sizeof(server)) == SOCKET_ERROR)
	{
		printf("\nNao e possivel construir o socket: %d", WSAGetLastError());
		exit(EXIT_FAILURE);
	}

	listen(s, 3);
	c = sizeof(struct sockaddr_in);

	while (1)
	{
		pos = qtdsockets;
		new_socket[qtdsockets++] = accept(s, (struct sockaddr *)&client, &c);
		if (new_socket[pos] == INVALID_SOCKET)
			printf("\nConexao nao aceita. Codigo de erro: %d", WSAGetLastError());

		else
		{
			puts("\nConexao aceita.");
			printf("\nDados do cliente - IP: %s -  Porta: %d\n", inet_ntoa(client.sin_addr), htons(client.sin_port));

			if (qtdsockets <= MAXSOCKETS)
				_beginthread(tratarConexao, NULL, pos);

			else
			{
				puts("\nNumero maximo de conexoes excedido!");
				strcpy(errormessage, "HTTP/1.1 429\r\nToo Many Requests\r\nContent-Type: text/html\r\nRetry-After: 60\r\n\r\n<HTML><H1>Numero maximo de conexoes excedido!</H1></HTML>\r\n");
				send(new_socket[pos], errormessage, strlen(errormessage) + 1, 0);
				closesocket(new_socket[pos]);
				qtdsockets--;
			}
		}
	}
	closesocket(s);
	WSACleanup();
}
