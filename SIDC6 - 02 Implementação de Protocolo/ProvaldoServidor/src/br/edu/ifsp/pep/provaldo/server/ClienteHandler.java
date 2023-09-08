package br.edu.ifsp.pep.provaldo.server;

import br.edu.ifsp.pep.provaldo.server.util.MontadorResposta;
import br.edu.ifsp.pep.provaldo.server.util.ValidadorDocumento;
import br.edu.ifsp.pep.provaldo.server.util.tipos.TipoDOCT;
import br.edu.ifsp.pep.provaldo.server.util.tipos.TipoDOCV;
import java.io.*;
import java.net.Socket;

public class ClienteHandler implements Runnable {

    private Socket socketCliente;
    private ClienteSocket clienteSocket;

    public ClienteHandler(ClienteSocket clienteSocket) {
        this.clienteSocket = clienteSocket;
    }

    public ClienteHandler(Socket socketCliente) {
        this.socketCliente = socketCliente;
    }

    @Override
    public void run() {
        String resposta = "";
        try {
            System.out.println("Cliente conectado: " + clienteSocket.obterEndereço());
            BufferedReader leitor = clienteSocket.getLeitor();
            String linha;

            while ((linha = leitor.readLine()) != null) {
                if (linha.equals("VALIDE")) {
                    String linhaNumDoc = leitor.readLine();
                    String numeroDocumento = ValidadorDocumento.parseNumeroDocumento(linhaNumDoc);
                    if (numeroDocumento.equalsIgnoreCase("")) {
                        resposta = MontadorResposta.gerarResposta(TipoDOCV.REQ_INVALIDO, numeroDocumento, TipoDOCT.NAO_AVALIADO);
                    } else {

                        String linhaTipoDoc = leitor.readLine();
                        TipoDOCT tipoDocumento = ValidadorDocumento.parseTipoDocumento(linhaTipoDoc);
                        TipoDOCV resultadoValidacao = ValidadorDocumento.validarDocumento(tipoDocumento, numeroDocumento);

                        resposta = MontadorResposta.gerarResposta(resultadoValidacao, numeroDocumento, tipoDocumento);
                    }
                } else {
                    resposta = MontadorResposta.gerarResposta(TipoDOCV.REQ_INVALIDO, "", TipoDOCT.NAO_AVALIADO);
                }
                clienteSocket.escritor(resposta);
            }

            ServidorProvaldo.getClientesSokets().remove(clienteSocket);
            clienteSocket.close();
            System.out.println("Cliente desconectado: " + clienteSocket.obterEndereço());
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
