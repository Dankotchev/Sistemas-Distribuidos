package br.edu.ifsp.pep.provaldo.server.util;

import br.edu.ifsp.pep.provaldo.server.util.tipos.TipoDOCT;
import br.edu.ifsp.pep.provaldo.server.util.tipos.TipoDOCV;
import br.edu.ifsp.pep.provaldo.server.util.api.validaCNPJ;
import br.edu.ifsp.pep.provaldo.server.util.api.validaCPF;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class ValidadorDocumento {

    public static TipoDOCT parseTipoDocumento(String linhaTipoDoc) {
        Pattern padrao = Pattern.compile("DOCT (\\d+)");
        Matcher correspondencia = padrao.matcher(linhaTipoDoc);
        if (correspondencia.find())
            return TipoDOCT.fromValor(Integer.parseInt(correspondencia.group(1)));
        return TipoDOCT.NAO_ESPECIFICADO;
    }

    public static String parseNumeroDocumento(String linhaNumDoc) {
        Pattern padrao = Pattern.compile("DOCN (.+)");
        Matcher correspondencia = padrao.matcher(linhaNumDoc);
        if (correspondencia.find())
            return correspondencia.group(1);
        return "";
    }

    public static TipoDOCV validarDocumento(TipoDOCT tipoDocumento, String numeroDocumento) {
        boolean valido = false;
        if (tipoDocumento == TipoDOCT.NAO_ESPECIFICADO)
            // Tipo de documento não suportado
            return TipoDOCV.DOC_INVALIDO;

        switch (tipoDocumento) {
            case CNPJ:
                valido = validaCNPJ.isCNPJ(numeroDocumento);
                break;
            case CPF:
                valido = validaCPF.isCPF(numeroDocumento);
                break;
            default:
                throw new AssertionError();
        }

        if (valido)
            return TipoDOCV.DOC_VALIDO;
        else
            return TipoDOCV.DOC_INVALIDO;
    }
}
