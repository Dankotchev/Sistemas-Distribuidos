package br.edu.ifsp.pep.provaldo.server;

import br.edu.ifsp.pep.provaldo.server.util.MontadorResposta;
import br.edu.ifsp.pep.provaldo.server.util.tipos.TipoDOCV;
import java.io.*;
import java.net.*;
import java.util.Queue;
import java.util.LinkedList;

public class ServidorProvaldo {

    private static Queue<ClienteSocket> clientesSokets = new LinkedList<>();

    public static void main(String[] args) {
        int porta = 12345;
        int maxConexoes = 15;

        try {
            ServerSocket servidorSocket = new ServerSocket(porta);
            System.out.println("Servidor TCP aguardando conexões na porta " + porta);

            while (true) {
                ClienteSocket clienteSocket = new ClienteSocket(servidorSocket.accept());
                //System.out.println("\nTAMANHO DA FILA: " + clientesSokets.size());

                if (clientesSokets.size() >= maxConexoes) {
                    System.out.println(
                            "Número máximo de conexões atingido. Rejeitando conexão de " + clienteSocket.obterEndereço());
                    String resposta = MontadorResposta.gerarResposta(TipoDOCV.CONX_MAX, "");
                    clienteSocket.escritor(resposta);
                    clienteSocket.close();
                } else {
                    clientesSokets.add(clienteSocket);
                    ClienteHandler ch = new ClienteHandler(clienteSocket);
                    Thread threadClienteHandler = new Thread(ch);
                    threadClienteHandler.start();
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static Queue<ClienteSocket> getClientesSokets() {
        return clientesSokets;
    }
}
