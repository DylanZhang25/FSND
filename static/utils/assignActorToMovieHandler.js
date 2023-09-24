// assignActorToMovieHandler.js

import { renderActorTable } from './actorManagementHandler.js';

let currentLayerIndex;
let loadingIndex;

/**
 * Initialize the event listener for the "star in" button and related functions.
 */
function initializeAssignActorToMovie() {
    document.addEventListener('click', function(event) {
        if (event.target.matches('.star-in-button')) {
            assignActorToMovie();
        }
    });
}

function assignActorToMovie() {
    const loadingIndex = layui.layer.load(1);
    fetchMoviesFromBackendEndpoint().then(function(movies) {
        layui.layer.close(loadingIndex);
        currentLayerIndex = layui.layer.open({
            type: 1,
            title: '<h4>Please click on the movie title to select a movie for this actor to appear in</h4>',
            area: ['550px', '600px'],
            content: createMovieContent(movies),
            success: function(layero, index) {
                addMovieClickListeners(layero, movies);  // Add click listeners after the content has been inserted into the DOM
            }
        });
    });
}

function fetchMoviesFromBackendEndpoint(page = 1, allMovies = []) {
    const token = sessionStorage.getItem('access_token');
    return axios.get('/api/movies', {
        params: {
            page: page,
        },
        headers: {
            Authorization: `Bearer ${token}`
        }
    })
    .then(function(response) {
        allMovies.push(...response.data.movies);

        if (page < response.data.pagination.pages) {
            // If there are more pages to fetch, recursively fetch the next page
            return fetchMoviesFromBackendEndpoint(page + 1, allMovies);
        } else {
            // All pages fetched, return the consolidated list of movies
            return allMovies;
        }
    })
    .catch(function(error) {
        console.error('Error fetching movies:', error);
        layui.layer.close(loadingIndex); // In case of error, close the loading layer
        return [];
    });
}

function createMovieContent(movies) {
    let content = '<div class="movies-container" style="display: flex; flex-wrap: wrap; justify-content: center;">';
    movies.forEach((movie, index) => {
        const movieElement = new DOMParser().parseFromString(movie.html, 'text/html').body.firstChild;
        const movieTitleElement = movieElement.querySelector('.movie-title-text');
        const newCardElement = document.createElement('div');
        newCardElement.className = 'layui-col-md5 layui-card layui-anim layui-anim-scale movie-card-background movie-card-transition';
        newCardElement.style.width = '96%';

        const newCardBodyElement = document.createElement('div');
        newCardBodyElement.className = 'layui-card movie-text-background';
        newCardBodyElement.appendChild(movieTitleElement);
        newCardElement.appendChild(newCardBodyElement);

        content += newCardElement.outerHTML;
    });
    content += '</div>';
    return content;
}

function addMovieClickListeners(layero, movies) {
    const movieCards = layui.jquery(layero).find('.movies-container').children();
    movieCards.each((index, card) => {
        layui.jquery(card).on('click', () => {
            starInMovie(movies[index].id);
        });

        layui.jquery(card).on('mouseover', () => {
            card.style.border = '3px solid #000d0b';  // Highlight border on mouseover
        });

        layui.jquery(card).on('mouseout', () => {
            card.style.border = '';  // Remove highlight on mouseout
        });
    });
}


function starInMovie(movieId) {
    const actorDataFromAssigning = localStorage.getItem('actorDataFromAssigning');
    const actorData  = JSON.parse(actorDataFromAssigning);
    const token = sessionStorage.getItem('access_token');
    let actorId = actorData.id;

    axios.post('/api/assign_actor_to_movie', {
        actor_id: actorId,
        movie_id: movieId
    }, {
        headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json'
        }
    })
    .then(function (response) {
        layui.layer.close(currentLayerIndex);
        layui.layer.msg(response.data.message, { time: 2000 });
        renderActorTable(); // Reload actor table data after successfully adding an actor to a movie
    })
    .catch(function (error) {
        layui.layer.msg(error.response.data.error, { time: 2000, icon: 5, shift: 6 });
    });
}

export { initializeAssignActorToMovie, assignActorToMovie };