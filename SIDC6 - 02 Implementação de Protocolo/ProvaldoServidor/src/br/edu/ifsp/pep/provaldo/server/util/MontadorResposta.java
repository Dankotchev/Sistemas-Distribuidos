package br.edu.ifsp.pep.provaldo.server.util;

import br.edu.ifsp.pep.provaldo.server.util.tipos.TipoDOCT;
import br.edu.ifsp.pep.provaldo.server.util.tipos.TipoDOCV;
import java.text.SimpleDateFormat;
import java.util.Date;

public class MontadorResposta {

    public static String gerarResposta(TipoDOCV resultadoValidacao, String numeroDocumento, TipoDOCT tipoDOCT) {
        SimpleDateFormat formatoData = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
        String dataAtual = formatoData.format(new Date());

        String resposta = "PROVALDO/0.2\r\n";
        resposta += "DTVD " + dataAtual + "\r\n";
        resposta += "DOCN " + numeroDocumento + "\r\n";
        resposta += "DOCT " + tipoDOCT.getValor() + "\r\n";
        resposta += "DOCV " + resultadoValidacao.getValor() + "\r\n";

        return resposta;
    }
}
