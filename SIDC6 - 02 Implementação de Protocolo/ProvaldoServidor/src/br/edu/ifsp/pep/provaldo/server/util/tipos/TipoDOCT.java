package br.edu.ifsp.pep.provaldo.server.util.tipos;

public enum TipoDOCT {
    NAO_ESPECIFICADO(0),
    CPF(1),
    CNPJ(2), 
    NAO_AVALIADO(9);

    private final int valor;

    TipoDOCT(int valor) {
        this.valor = valor;
    }

    public int getValor() {
        return valor;
    }

    public static TipoDOCT fromValor(int valor) {
        for (TipoDOCT tipo : values()) {
            if (tipo.getValor() == valor)
                return tipo;
        }
        return NAO_ESPECIFICADO;
    }
}
