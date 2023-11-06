const soap = require("soap");
const url = "http://localhost:8000/MoviesService?wsdl";
const readline = require("readline");

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
});

const args = {
  nome: "Nome",
  ano: 2000,
  genero: "Genero",
};

soap.createClient(url, function (erro, cliente) {
  if (erro) {
    console.error(erro);
    return;
  }

  function displayMenu() {
    console.log("Escolha uma operação:");
    console.log("1. Buscar filmes por nome");
    console.log("2. Buscar filmes por ano");
    console.log("3. Buscar filmes por gênero");
    console.log("4. Sair");
    rl.question("Digite o número da operação desejada: ", function (escolha) {
      switch (escolha) {
        case "1":
          getMoviesByName();
          break;
        case "2":
          getMoviesByYear();
          break;
        case "3":
          getMoviesByGenre();
          break;
        case "4":
          rl.close();
          break;
        default:
          console.log("Opção inválida. Tente novamente.");
          displayMenu();
      }
    });
  }

  function getMoviesByName() {
    rl.question("Digite o nome do filme: ", function (nome) {
      args.nome = nome;
      cliente.getMoviesByName(args, function (erro, resultado) {
        if (erro) console.error(erro);
        else console.log("Filmes por nomes:", resultado);

        displayMenu();
      });
    });
  }

  function getMoviesByYear() {
    rl.question("Digite o ano: ", function (ano) {
      args.ano = parseInt(ano);
      cliente.getMoviesByYear(args, function (erro, resultado) {
        if (erro) console.error(erro);
        else console.log("Filmes por ano de Lançamento:", resultado);

        displayMenu();
      });
    });
  }

  function getMoviesByGenre() {
    rl.question("Digite o gênero: ", function (genero) {
      args.genero = genero;
      cliente.getMoviesByGenre(args, function (erro, resultado) {
        if (erro) console.error(erro);
        else console.log("Filmes por gêneros:\n", resultado);

        displayMenu();
      });
    });
  }

  displayMenu();
});
