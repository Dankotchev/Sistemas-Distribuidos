const soap = require('soap');
const http = require('http');

// Simula um banco de dados em memória
const movieDatabase = [
    { name: "Filme #1", year: 2000, genre: "Ação" },
    { name: "Filme #2", year: 2005, genre: "Drama" },
    { name: "Filme #3", year: 2010, genre: "Comedia" },
    { name: "Filme #4", year: 2000, genre: "Drama" },
    { name: "Filme #5", year: 2005, genre: "Ação" },
    { name: "Filme #6", year: 2010, genre: "Comedia" },
    { name: "Filme #7", year: 2000, genre: "Ação" },
    { name: "Filme #8", year: 2005, genre: "Drama" },
    { name: "Filme #9", year: 2010, genre: "Comedia" },
];

const service = {
    MoviesService: {
        MoviesPort: {
            getMoviesByName: function(args, callback) {
                const name = args.name;
                const filteredMovies = movieDatabase.filter(movie => movie.name === name);
                const movieNames = filteredMovies.map(movie => movie.name);
                callback(null, { movies: movieNames });
            },
            getMoviesByYear: function(args, callback) {
                const year = args.year;
                const filteredMovies = movieDatabase.filter(movie => movie.year === year);
                const movieNames = filteredMovies.map(movie => movie.name);
                callback(null, { movies: movieNames });
            },
            getMoviesByGenre: function(args, callback) {
                const genre = args.genre;
                const filteredMovies = movieDatabase.filter(movie => movie.genre === genre);
                const movieNames = filteredMovies.map(movie => movie.name);
                callback(null, { movies: movieNames });
            },
        },
    },
};

const xml = require('fs').readFileSync('MoviesService.wsdl', 'utf8');

const server = http.createServer(function(request, response) {
    response.end('404: Not Found: ' + request.url);
});

server.listen(8000);
soap.listen(server, '/MoviesService', service, xml);
