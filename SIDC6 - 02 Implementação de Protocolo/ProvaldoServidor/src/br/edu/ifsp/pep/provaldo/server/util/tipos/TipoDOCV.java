package br.edu.ifsp.pep.provaldo.server.util.tipos;


public enum TipoDOCV {
    DOC_INVALIDO(100), DOC_VALIDO(110),
    TIPO_DOC_INVALIDO(200),
    REQ_INVALIDO(300),
    CONX_MAX(400),
    VALID_NAO_ESPEC(999);

    private final int valor;

    TipoDOCV(int valor) {
        this.valor = valor;
    }

    public int getValor() {
        return valor;
    }

    public static TipoDOCV fromValor(int valor) {
        for (TipoDOCV tipo : values()) {
            if (tipo.getValor() == valor)
                return tipo;
        }
        return VALID_NAO_ESPEC;
    }
}
