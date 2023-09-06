import socket
import threading

def enviar_solicitacao():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((servidor_ip, servidor_porta))

        s.sendall(b'VALIDE\r\n')
        s.sendall(f'DOCN {numero_documento}\r\n'.encode())
        s.sendall(f'DOCT {tipo_documento}\r\n'.encode())

        resposta = s.recv(1024).decode()
        print("Resposta do servidor:")
        print(resposta)

def main():
    global servidor_ip, servidor_porta, numero_documento, tipo_documento

    servidor_ip = 'localhost'
    servidor_porta = 12345

    numero_documento = input("Digite o número do documento: ")
    tipo_documento = int(input("Digite o tipo do documento (1 para CPF, 2 para CNPJ): "))

    # Crie uma thread para a função enviar_solicitacao
    while True:
        thread = threading.Thread(target=enviar_solicitacao)
        thread.start()


    # Você pode continuar executando outras tarefas aqui na thread principal, se necessário.

if __name__ == "__main__":
    main()
