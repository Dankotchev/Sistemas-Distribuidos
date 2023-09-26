var grpc = require("@grpc/grpc-js");
const protoLoader = require("@grpc/proto-loader");
const readline = require("readline");

const PROTO_PATH = "../protos/provaldo.proto";
const packageDefinition = protoLoader.loadSync(PROTO_PATH);
const provaldo = grpc.loadPackageDefinition(packageDefinition).provaldo;

const client = new provaldo.Validador(
	"localhost:1996",
	grpc.credentials.createInsecure()
);

const rl = readline.createInterface({
	input: process.stdin,
	output: process.stdout,
});

function valoresDOCT(doct) {
	switch (doct) {
		case 0:
			return "Não especificado";
		case 1:
			return "CPF";
		case 2:
			return "CNPJ";
		case 9:
			return "Não avaliado";
	}
}

function valoresDOCV(docv) {
	switch (docv) {
		case 100:
			return "Documento inválido";
		case 110:
			return "Documento válido";
		case 200:
			return "Tipo Inválido";
		case 300:
			return "Requisição Inválida";
		case 400:
			return "Conexões máximas atingidas";
		case 999:
			return "Não especificado";
	}
}

function lerInfoDocumento(callback) {
	rl.question("Digite o número do documento (CPF ou CNPJ): ", (docn) => {
		rl.question(
			"Digite o tipo do documento (1 para CPF ou 2 para CNPJ): ",
			(doct) => {
				const request = {
					docn: docn,
					doct: parseInt(doct),
				};
				rl.close();
				callback(request);
			}
		);
	});
}

function apresentarRespota(resposta) {
	DOCT = valoresDOCT(resposta.doct);
	DOCV = valoresDOCV(resposta.docv);

	console.log("Data de Validade:", resposta.dtvd);
	console.log("Número do Documento:", resposta.docn);
	console.log("Tipo do Documento:", DOCT);
	console.log("Resposta:", DOCV);
}

function run() {
	lerInfoDocumento((request) => {
		client.Validar(request, (error, response) => {
			if (!error)
				apresentarRespota(response);
			else
				console.error("Erro ao chamar o método:", error);
		});
	});
}

run();
