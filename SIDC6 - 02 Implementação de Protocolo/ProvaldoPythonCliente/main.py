import socket

def tratar_resposta(resposta):
    linhas = resposta.split('\r\n')

    # Processar cada linha para extrair informações relevantes
    data_validacao = ""
    numero_documento = ""
    codigo_resultado = ""

    for linha in linhas:
        if linha.startswith("DTVD"):
            data_validacao = linha.split(' ', 1)[1]
        elif linha.startswith("DOCN"):
            numero_documento = linha.split(' ', 1)[1]
        elif linha.startswith("DOCV"):
            codigo_resultado = int(linha.split(' ', 1)[1])

    mensagens = {
        100: "Documento inválido",
        110: "Documento válido",
        200: "Tipo de documento inválido",
        300: "Requisição inválida",
        400: "Conexões máximas atingidas"
    }

    # Imprimir as informações de forma clara
    print("Data de validação:", data_validacao)
    print("Número do documento:", numero_documento)
    print("Resultado da validação:", codigo_resultado, "-", mensagens.get(codigo_resultado, "Código de resultado desconhecido"))


def main():
    # Endereço do servidor e porta
    servidor_ip = 'localhost'  # IP do servidor
    servidor_porta = 12345    # Porta do servidor

    # Criação do socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((servidor_ip, servidor_porta))

        # Entrada do usuário
        numero_documento = input("Digite o número do documento: ")
        tipo_documento = int(input("Digite o tipo do documento (1 para CPF, 2 para CNPJ): "))

        # Envio da solicitação para o servidor
        s.sendall(b'VALIDE\r\n')
        s.sendall(f'DOCN {numero_documento}\r\n'.encode())
        s.sendall(f'DOCT {tipo_documento}\r\n'.encode())

        # Recebimento e impressão da resposta do servidor
        print("\n\n---\n\n")
        resposta = s.recv(1024).decode()
        tratar_resposta(resposta)

if __name__ == "__main__":
    main()
