// moviesRenderHandler.js

// Rendering movie listings and pagination
function renderMovieList(page) {
    const $ = layui.jquery;
    const token = sessionStorage.getItem('access_token');

    if (token) {
        axios({
            method: 'get',
            url: `/api/movies?page=${page}`,
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            console.log('Received movie data: ', response.data);
            const movies = response.data.movies;
            const pagination = response.data.pagination;

            const movieListContainer = $('#movie-list-div');
            movieListContainer.empty();

            // Use JQuery to insert rendered HTML received from the backend into the DOM instead of manually creating HTML strings
            movies.forEach(function (movie) {
                movieListContainer.append(movie.html);
            });

            // Load the pagination method
            renderPagination(pagination);
        })
        .catch(error => {
            console.error('Error:', error);
            layer.msg('Failed to load movies data, please try again.', { icon: 2 });
        });
    } else {
        console.error("No token found in session storage");
    }
}

// Movies Pagination Controls
function renderPagination(pagination) {
    layui.laypage.render({
        elem: 'pagination',
        curr: pagination.page,
        count: pagination.total,
        limit: pagination.per_page,
        layout: ['prev', 'page', 'next', 'skip', 'count'],
        prev: '<',
        next: '>',
        jump: function (obj, first) {
            if (!first) {
                renderMovieList(obj.curr);
            }
        }
    });
}

export { renderMovieList, renderPagination };