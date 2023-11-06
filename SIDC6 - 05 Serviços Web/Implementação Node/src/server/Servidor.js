const soap = require("soap");
const http = require("http");

// Simula um banco de dados em memória
const movieDatabase = [
  { nome: "Filme #1", ano: 2000, genero: "Ação" },
  { nome: "Filme #2", ano: 2005, genero: "Drama" },
  { nome: "Filme #3", ano: 2010, genero: "Comedia" },
  { nome: "Filme #4", ano: 2000, genero: "Drama" },
  { nome: "Filme #5", ano: 2005, genero: "Ação" },
  { nome: "Filme #6", ano: 2010, genero: "Comedia" },
  { nome: "Filme #7", ano: 2000, genero: "Ação" },
  { nome: "Filme #8", ano: 2010, genero: "Drama" },
];

const service = {
  MoviesService: {
      MoviesPort: {
          getMoviesByName: function(args, callback) {
              const nome = args.nome;
              const filtroFilmes = movieDatabase.filter(filme => new RegExp(nome, 'i').test(filme.nome));
              callback(null, filtroFilmes);
          },
          getMoviesByYear: function(args, callback) {
              const ano = args.ano;
              const filtroFilmes = movieDatabase.filter(filme => filme.ano == ano);
              callback(null, filtroFilmes);
          },
          getMoviesByGenre: function(args, callback) {
              const genero = args.genero;
              const filtroFilmes = movieDatabase.filter(movie => movie.genero === genero);
              callback(null, filtroFilmes);
          },
      },
  },
};

const xml = require("fs").readFileSync("src/MoviesService.wsdl", "utf8");

const server = http.createServer(function (request, response) {
  response.end("404: Not Found: " + request.url);
});

server.listen(8000);
soap.listen(server, "/MoviesService", service, xml);
