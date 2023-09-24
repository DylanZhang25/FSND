/**
 * jwtTokenAndUserLoginHandler.js
 *
 * This script handles user login and logout processes, along with JWT token processing from Auth0.
 */


// Hide all functionality tabs (the left Navigator menu) when the page initially loads.
// (function() {
//     // Hide all functionality tabs (the left Navigator menu) when the page initially loads
//     document.getElementById('side-nav').style.display = 'none';
//     document.getElementById('actors-management-tab').style.display = 'none';
//     document.getElementById('movies-management-tab').style.display = 'none';
// })();

/**
 * Get the URL address in the browser's address bar which is sent by Auth0 after a user has successfully logged in.
 * Example:
 *     Auth0 callback URL: "http://127.0.0.1:5000"
 *     The format of the URL address in the browser: "http://127.0.0.1:5000/#access_token=this-is-a-demo-token"
 */
const fragment = window.location.hash.substr(1);
let params = {};
// Parsing parameters in URL
fragment.split('&').forEach(function (item) {
    var parts = item.split('=');
    params[parts[0]] = parts[1];
});

/**
 * ### User Login function:
 * Processes the JWT token from Auth0 after a user has successfully logged in:
 *  1. The token is stored in the front-end sessionStorage.
 *  2. Originally, a JWT token does not contain user information. However, by modifying the Auth0 Rules to add "Add email to access token", the access_token from Auth0 now contains a separate field named "castingagency-user-email" in the JWT payload. This property can be stored on the front-end and presented as the user's name after logging in.
 *  3. After storing the access_token on the front-end, it is sent to the back-end endpoint (@app.route('/post_token_to_backend', methods=['POST'])) for authorization purposes in other endpoints.
 */
function storeTokenInFrontedAndSendItToBackend () {
    // Store the access_token
    let accessToken = params.access_token;
    if (accessToken) {
        // Store the access_token on the frontend for subsequent use. It can be stored in sessionStorage or localStorage.
        sessionStorage.setItem('access_token', accessToken);
        console.log('Token stored in index.html:', accessToken);
        updateUserInfo(accessToken);


        // For security reasons, hide access_token data in the address bar of the user's browser.
        let remainingData = {};
        for (let key in params) {
            if (key !== 'access_token') {
                remainingData[key] = params[key];
            }
        }
        console.log('Access Token:', accessToken);

        // Modify the browser's address bar to keep only the base URL section.
        window.location.hash = '';
        window.history.pushState({}, document.title, window.location.pathname);

        /**
         * The jwt token is sent via the Authorization header and must contain the following format when sent from the front-end to the back-end.
            headers: {
                'Authorization': `Bearer ${accessToken}`
            }
        * Otherwise, the backend jwt will not recognize the jwt without the Authorization header, leading to errors like "jose.exceptions.JWTError: Error decoding token headers.
        */
        axios.post('/post_token_to_backend', {}, {
            headers: {
                'Authorization': `Bearer ${accessToken}`
            }
        })
        .then(function (response) {
            if (response.status === 200) {
                console.log('Access token sent to the backend successfully.');
            } else {
                console.error('Failed to send access token to the backend.');
            }
        })
        .catch(function (error) {
            console.error('Error sending access token:', error);
        });

    } else {
        // If the page is refreshed, try to get the access_token from sessionStorage, so that the user stays logged in after refreshing the page.
        accessToken = sessionStorage.getItem('access_token');
        if (accessToken) {
            updateUserInfo(accessToken);
        }
    }
}

function parseJwt(token) {
    const base64Url = token.split('.')[1];
    const base64 = decodeURIComponent(atob(base64Url).split('').map((c) => {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));
    return JSON.parse(base64);
}

function updateUserInfo(accessToken) {
    // If the page is refreshed, try to get the access_token from sessionStorage, so that the user stays logged in after refreshing the page.
    if (!accessToken) {
        accessToken = sessionStorage.getItem('access_token'); // 假设 accessToken 存储在 sessionStorage 中
    }

    // Get Page Elements in the DOM.
    const loginModel = document.getElementById('login-model');
    const userInfoModel = document.getElementById('user-info-model');

    // Get user login and user information blocks.
    const loginBlock = document.getElementById('login-block');
    const userInfoBlock = document.getElementById('user-info-block');

    // Get "User Name" related elements.
    const userNameLink = document.getElementById('user-name-link');
    const userNameText = document.getElementById('user-name-text');

    if (accessToken) {
        const decodedToken = parseJwt(accessToken); // Parsing the accessToken.
        const userEmail = decodedToken['castingagency-user-email'];
        const userPermissions = decodedToken['permissions'];

        // Print userEmail and userPermissions for testing
        console.log('userEmail:', userEmail);
        console.log('userPermissions:', userPermissions);

        // Hide user login block, show user info block.
        loginModel.style.display = 'none';
        userInfoModel.style.display = 'block';

        document.getElementById('side-nav').style.display = 'block';
        // Show left side tabs based on permissions.
        if (
            userPermissions.includes('delete:actor') &&
            userPermissions.includes('get:actors') &&
            userPermissions.includes('patch:actor') &&
            userPermissions.includes('post:actor')
        ) {
            document.getElementById('actors-management-tab').style.display = 'block';
        }

        if (userPermissions.includes('get:movies')) {
            document.getElementById('movies-management-tab').style.display = 'block';
        }

        // Set the values of "castingagency-user-email" to be the user's name presented on user info block.
        const userName = decodedToken['castingagency-user-email'];
        // Update the content of the user's name text on user info block.
        userNameText.textContent = userName;
    } else {
        // If accessToken does not exist, show the user login block and hide the user info block.
        loginModel.style.display = 'block';
        userInfoModel.style.display = 'none';
    }
}

/**
 * ### User Logout function:
 * Handles the logout action on both the front-end and the back-end:
 *  1. Clears the data in localStorage and sessionStorage.
 *  2. Sends a request to the back-end endpoint (@app.route('/api/logout', methods=['GET'])) and redirects users to the Auth0 logout URL.
 */
function initLogoutModule() {
    document.getElementById('sign-out-link').addEventListener('click', handleLogout);
}

function handleLogout() {
    localStorage.clear();
    sessionStorage.clear();
    window.location.href = '/api/logout';
}

// Initialize the "initLogoutModule" and "storeTokenInFrontedAndSendItToBackend" after the DOM has been fully loaded.
document.addEventListener('DOMContentLoaded', (event) => {
    document.getElementById('side-nav').style.display = 'none';
    document.getElementById('actors-management-tab').style.display = 'none';
    document.getElementById('movies-management-tab').style.display = 'none';
    initLogoutModule();
    storeTokenInFrontedAndSendItToBackend();
});

/**
 * This function retrieves the JWT from the sessionStorage.
 * @returns {string} - The JWT of the user.
 */
function getUserJWT() {
    var jwt = sessionStorage.getItem('access_token');
    return jwt;
}

/**
 * This function creates a pop-up using Layui to display the user's JWT.
 */
function initializeJWTDisplayPopup() {
    document.getElementById('show-jwt-link').addEventListener('click', function() {
        var jwt = getUserJWT();
        var jwtLength = jwt ? jwt.length : 0;
        var width = Math.min(jwtLength * 10, 1200) + 'px';

        layer.open({
            type: 1,
            title: 'Your JWT',
            content: '<div style="padding: 20px;">' + jwt + '</div>',
            area: [width, 'auto']
        });
    });
}

document.addEventListener('DOMContentLoaded', (event) => {
    initializeJWTDisplayPopup();
});