package br.edu.ifsp.pep.provaldo.server;

import java.io.*;
import java.net.InetAddress;
import java.net.Socket;

public class ClienteSocket {

    private final Socket socketCliente;
    private InputStream entrada;
    private OutputStream saida;
    private BufferedReader leitor;
    private PrintWriter escritor;

    public ClienteSocket(Socket socketCliente) {
        this.socketCliente = socketCliente;
    }

    public BufferedReader getLeitor() {
        try {
            this.entrada = socketCliente.getInputStream();
            this.leitor = new BufferedReader(new InputStreamReader(entrada, "UTF-8"));
        } catch (UnsupportedEncodingException ex) {
            ex.printStackTrace();
        } catch (IOException ex) {
            ex.printStackTrace();
        }
        return leitor;
    }

    public void escritor(String mensagem) {
        try {
            this.saida = socketCliente.getOutputStream();
            this.escritor = new PrintWriter(new OutputStreamWriter(saida, "UTF-8"), true);
            this.escritor.println(mensagem);
        } catch (UnsupportedEncodingException ex) {
            ex.printStackTrace();
        } catch (IOException ex) {
            ex.printStackTrace();
        }
    }

    public InetAddress obterEndereço() {
        return this.socketCliente.getInetAddress();
    }

    public void close() {
        try {
            this.socketCliente.close();
        } catch (IOException ex) {
            ex.printStackTrace();
        }
    }
}
