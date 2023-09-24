from datetime import datetime
from math import ceil

from flask import Flask, request, render_template, jsonify, redirect, abort, \
    url_for
from sqlalchemy import asc
from sqlalchemy.exc import SQLAlchemyError, OperationalError, IntegrityError
from distutils.util import strtobool
from sqlalchemy.orm import joinedload

import config
from config import DatabaseConfig, Auth0Config
from extensions import register_extension, db
from models import Actor, Movie
from models import ActorMovieAssociation as actor_movie_association
from jose import jwt
from urllib.request import urlopen
import json
from functools import wraps


def create_app():
    """
    In the real project, testing database and deployment database must be
    seperated, but in this project, I would like to assume all the postgres
    databases are the same one which is creating and hosting on Render.com.
    """
    from config import DatabaseConfig
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = (
        DatabaseConfig.SQLALCHEMY_DATABASE_URI
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = (
        DatabaseConfig.SQLALCHEMY_TRACK_MODIFICATIONS
    )
    app.config['AUTH0_AUDIENCE'] = Auth0Config.AUTH0_AUDIENCE
    app.config['AUTH0_RESPONSE_TYPE_ACCESS_TOKEN'] = (
        Auth0Config.AUTH0_RESPONSE_TYPE_ACCESS_TOKEN
    )
    app.config['AUTH0_RESPONSE_TYPE_ID_TOKEN'] = (
        Auth0Config.AUTH0_RESPONSE_TYPE_ID_TOKEN
    )
    app.config['AUTH0_CLIENT_ID'] = Auth0Config.AUTH0_CLIENT_ID
    app.config['AUTH0_REDIRECT_URI'] = Auth0Config.AUTH0_REDIRECT_URI
    app.config['AUTH0_DOMAIN'] = Auth0Config.AUTH0_DOMAIN
    app.config['AUTH0_ALGORITHMS'] = Auth0Config.AUTH0_ALGORITHMS

    # Using a function in extensions.py to initiate database.
    register_extension(app)

    return app


app = create_app()


# Load configuration from object
# app.config.from_object('config.DatabaseConfig')

# test the auth0_url
auth0_url_for_id_token = Auth0Config.get_auth0_url_for_id_token()
auth0_url_for_access_token = Auth0Config.get_auth0_url_for_access_token()
# print("auth0_url_for_id_token is: " + auth0_url_for_id_token)
# print("auth0_url_for_access_token: " + auth0_url_for_access_token)


@app.get('/actor_add')
def actor_add():
    return render_template('actor_add.html')


@app.get('/actor_edit')
def actor_edit():
    return render_template('actor_edit.html')


@app.route('/login')
def user_login():
    return redirect(auth0_url_for_access_token)


'''
@COMPLETED_5
API Architecture and Testing

CRITERIA:
- Enable Role Based Authentication and roles-based access control (RBAC) 
  in a Flask application.

MEETS SPECIFICATIONS:
- Project includes a custom @requires_auth decorator that:
    - get the Authorization header from the request
    - Decode and verify the JWT using the Auth0 secret
    - take an argument to describe the action
    - raise an error if:
      - the token is expired
      - the claims are invalid
      - the token is invalid
      - the JWT doesn’t contain the proper action
- Project includes at least two different roles that have distinct 
  permissions for actions. These roles and permissions are clearly defined 
  in the project README. 
'''


@app.route('/post_token_to_backend', methods=['POST'])
def store_access_token():
    """ Get and Store the access_token from frontend """
    # 从Authorization头中获取访问令牌
    auth_header = request.headers.get('Authorization')
    # print('store_access_token() auth_header: ', auth_header)
    if auth_header:
        access_token = auth_header.split(' ')[1]
        # print('store_access_token() Extracted token: ', access_token)
    else:
        access_token = None

    if access_token:
        # print('store_access_token() ---> Access Token: ', access_token)
        return access_token
    else:
        return 'Access Token Not Found in Request'


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def check_permissions(permission, payload):
    # print(f"Permission to check: {permission}")
    # print(f"Payload type: {type(payload)}")
    # print(f"Payload content: {payload}")
    # print(f"Permissions in payload: {payload.get('permissions')}")

    if 'permissions' not in payload:
        print("No permissions in payload")
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permissions not found in JWT'
        }, 400)

    if permission not in payload['permissions']:
        print(f"Permission {permission} not in payload permissions")
        raise AuthError(
            {
                'code': 'forbidden',
                'description': 'Permission not found'
            }, 403)

    return True


def verify_decode_jwt(token):
    """
    Validate a request using an Auth0 issued JWT.
    If there is a valid JWT, return the payload og the JWT as the result.
    """
    print(f"Token received for verification: {token}")
    jsonurl = urlopen(
        f'https://{Auth0Config.AUTH0_DOMAIN}/.well-known/jwks.json'
    )
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=Auth0Config.AUTH0_ALGORITHMS,
                audience=Auth0Config.AUTH0_AUDIENCE,
                issuer='https://' + Auth0Config.AUTH0_DOMAIN + '/'
            )
            # Check the current token's infos as contents and expiry time.
            print('Token is valid, please see the following details: ')
            print('verify_decode_jwt(token) ---> Decoded payload:', payload)
            print('Token contents:', payload)
            print('Token expiry time:', datetime.utcfromtimestamp(
                payload["exp"]))
            print('Current server time:', datetime.utcnow())

            return payload

        except jwt.ExpiredSignatureError as e:
            print(f"ExpiredSignatureError during token decode: {e}")
            print('Token has expired, please see the following details: ')
            payload_without_expiration_verification = jwt.decode(
                token, rsa_key,
                algorithms=Auth0Config.AUTH0_ALGORITHMS,
                audience=Auth0Config.AUTH0_AUDIENCE,
                issuer='https://' + Auth0Config.AUTH0_DOMAIN + '/',
                options={"verify_exp": False}
            )
            print('Token contents:', payload_without_expiration_verification)
            print('Token expiry time:', datetime.utcfromtimestamp(
                payload_without_expiration_verification["exp"]))
            print('Current server time:', datetime.utcnow())
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Check the audience&issuer.'
            }, 401)
        except Exception as e:
            print(f"Exception during token decode: {e}")
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 400)


def requires_auth(permission=''):
    """ A custom @requires_auth decorator """
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            # print(f"args: {args}")
            # print(f"kwargs: {kwargs}")
            try:
                token = store_access_token()
                payload = verify_decode_jwt(token)
                check_permissions(permission, payload)
                return f(payload, *args, **kwargs)
            except AuthError as ae:
                # print(f" -> Auth error occurred: {ae.error}")
                abort(ae.status_code, ae.error)
        return wrapper
    return requires_auth_decorator


@app.route('/')
def home_page():  # put application's code here
    return render_template('index.html')


def generate_demo_database_data():
    """Generate demo data for Flask CLI."""
    db.drop_all()
    db.create_all()
    from faker import Faker
    faker = Faker(locale="en-US")

    for i in range(30):
        actor = Actor()
        info = faker.simple_profile()
        actor.name = info['name']
        actor.age = faker.random_int(min=18, max=100)
        actor.save()

    for i in range(30):
        movie = Movie()
        movie.title = faker.sentence(nb_words=4)
        movie.date = faker.date_this_decade()
        movie.save()


@app.cli.command("create_a_demo_database_cli")
def create_a_demo_database_cli():
    """Flask CLI command to generate demo data."""
    generate_demo_database_data()


'''
@COMPLETED_2
Data Modeling

CRITERIA:
- Utilize SQLAlchemy to conduct database queries

MEETS SPECIFICATIONS:
- Does not use raw SQL or only where there are not SQLAlchemy equivalent 
  expressions.
- Correctly applies SQLAlchemy to define models and data types.
- Creates methods to serialize model data and helper methods to simplify 
  API behavior such as insert, update and delete.
'''


'''
@COMPLETED_3
API Architecture and Testing

CRITERIA:
- Follow RESTful principles of API development

MEETS SPECIFICATIONS:
- RESTful principles are followed throughout the project, including appropriate
  naming of endpoints, use of HTTP methods GET, POST, PATCH, and DELETE.
- Routes perform CRUD operations
'''


'''
@COMPLETED_4
API Architecture and Testing

CRITERIA:
- Structure endpoints to respond to 4 HTTP methods, including error handling.

MEETS SPECIFICATIONS:
- Specifies endpoints and behavior for at least:
    - Two GET requests
    - One POST request
    - One PATCH request
    - One DELETE request
'''


@app.route('/api/actors', methods=['GET'])
@requires_auth('get:actors')
def get_actors(payload):
    try:
        page = request.args.get('page', type=int, default=1)
        query = Actor.query.order_by(asc(Actor.id))
        query_an_actor_by_name = db.select(Actor)
        user_input_name = request.args.get('name')
        """
        Different query operations are performed depending on 
        whether or not the user has provided an actor name:
            If the actor name is provided, it is filtered by name and paged,
            otherwise it is sorted by actor ID in ascending order and paged.
        """
        if user_input_name:
            query_an_actor_by_name = query_an_actor_by_name.where(
                Actor.name.ilike(f"%{user_input_name}%")
            )  # fuzzy query with non-case-sensitive
            paginate = db.paginate(query_an_actor_by_name,
                                   page=page, per_page=10, error_out=False)
        else:
            paginate = query.paginate(page=page, per_page=10, error_out=False)

        items: [Actor] = paginate.items
        actor_data = []

        for item in items:
            # query about the movies in which an actor will act
            movie_titles = db.session.query(Movie.title) \
                .join(actor_movie_association,
                      Movie.id == actor_movie_association.movie_id) \
                .filter(actor_movie_association.actor_id == item.id) \
                .all()
            movie_titles = [movie[0] for movie in movie_titles]

            actor_data.append({
                'id': item.id,
                'name': item.name,
                'age': item.age,
                'is_time_available': item.is_time_available,
                'create_at': item.create_at.strftime('%Y-%m-%d %H:%M:%S'),
                'update_at': item.update_at.strftime('%Y-%m-%d %H:%M:%S'),
                'movies': movie_titles
            })

        return {
            'code': 0,
            'msg': 'actor query success',
            'count': paginate.total,
            'data': actor_data
        }
    except SQLAlchemyError as e:
        abort(500, description=f"Database error: {str(e)}")


@app.route('/api/actor', methods=['POST'])
@requires_auth('post:actor')
def add_a_new_actor(payload):
    data = request.get_json()
    print(data)
    # Validate required fields in the data.
    if not data or \
            'name' not in data or \
            'age' not in data or \
            'is_time_available' not in data or \
            'create_at' not in data:
        abort(400, description="The Data Is Missing required fields.")

    # Convert 'true' or 'false' strings to actual boolean values
    is_time_available_str = data.get('is_time_available', '').lower()
    data['is_time_available'] = bool(strtobool(is_time_available_str))

    actor = Actor()
    actor.update(data)

    try:
        actor.save()
    except IntegrityError as e:
        db.session.rollback()
        abort(400, description=f"Integrity Error: {e}")
    except Exception as e:
        print("(add_a_new_actor) except Exception as e: ")
        print(e)
        db.session.rollback()
        abort(500, description=f"Unexpected error: {e}")

    # Calculate the page number where the new actor will appear,
    # And jump to the last page of the actor table on the frontend,
    # Because id self-incrementing within the database.
    items_per_page = 10
    total_actors_count = Actor.query.count()
    total_pages = ceil(total_actors_count / items_per_page)

    return {
        'code': 0,
        'msg': 'Succeeded in adding data',
        'page_number': total_pages,
        'count': total_actors_count
        # Return the page number where the new actor will appear
    }, 201


@app.route('/api/actor/<int:aid>', methods=['PATCH'])
@requires_auth('patch:actor')
def patch_an_actor(payload, aid):
    data = request.get_json()
    is_time_available_str = data.get('is_time_available', '').lower()
    data['is_time_available'] = bool(strtobool(is_time_available_str))

    actor = Actor.query.get(aid)
    if actor is None:
        abort(404, description='Actor not found')

    actor.update(data)

    try:
        actor.save()
    except IntegrityError as e:
        db.session.rollback()
        abort(400, description=f"Integrity Error: {e}")
    except Exception as e:
        db.session.rollback()
        abort(500, description=f"Unexpected error: {e}")

    return jsonify({
        'code': 0,
        'msg': 'Succeeded in editing data'
    }), 200


@app.route('/api/actor/<int:aid>', methods=['DELETE'])
@requires_auth('delete:actor')
def delete_an_actor(payload, aid):
    actor = Actor.query.get(aid)
    if actor is None:
        abort(404)

    try:
        db.session.delete(actor)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({
            'code': -1,
            'msg': 'Failed to delete data due to Integrity Error',
            'error': str(e)
        }), 400
    except Exception as e:
        db.session.rollback()
        abort(500, description=str(e))
    return jsonify({
        'code': 0,
        'msg': 'Succeeded in deleting data'
    }), 200


@app.route('/api/movies', methods=['GET'])
@requires_auth('get:movies')
def get_movies(payload):
    try:
        page = request.args.get('page', default=1, type=int)
        per_page = 8

        query = Movie.query \
            .options(joinedload(Movie.actor_associations).joinedload(
            actor_movie_association.actor)) \
            .order_by(Movie.date.desc())

        movies = query.paginate(page=page, per_page=per_page, error_out=False)

        movie_data = []
        for movie in movies.items:
            movie_info = {
                'id': movie.id,
                'title': movie.title,
                'date': movie.date.strftime('%Y-%m-%d') if movie.date else '',
                'actors': [association.actor.name for association in
                           movie.actor_associations]
            }

            # Renders the Jinja2 template
            # and sends the rendered HTML as part of the response
            movie_html = render_template(
                'movie_card.html',
                movie=movie_info
            )
            movie_info['html'] = movie_html
            movie_data.append(movie_info)

        # Building Pagination Information
        pagination = {
            'page': movies.page,
            'per_page': per_page,
            'total': movies.total,
            'pages': movies.pages
        }

        return jsonify({'movies': movie_data, 'pagination': pagination})
    except OperationalError:
        abort(500)  # If there is a database operation error
    except Exception as e:
        # Catch any other exceptions and trigger a 400 error handler
        abort(400, description=str(e))


@app.route('/api/logout', methods=['GET'])
def logout():
    """ User Logout endpoint """
    domain = Auth0Config.AUTH0_DOMAIN
    client_id = Auth0Config.AUTH0_CLIENT_ID

    # Building Auth0 Logout URL
    auth0_logout_url = (
        f'https://{domain}/v2/logout'
        f'?client_id={client_id}'
        f'&returnTo={url_for("home_page", _external=True)}'
    )
    # print("auth0_logout_url is: ", auth0_logout_url)

    # Redirect users to the Auth0 logout URL
    return redirect(auth0_logout_url)


@app.route('/api/assign_actor_to_movie', methods=['POST'])
@requires_auth('patch:actor')
def assign_actor_to_movie(payload):
    """ Assign an actor to a movie to act in """
    try:
        data = request.get_json()
        actor_id = data.get('actor_id')
        movie_id = data.get('movie_id')

        # Check if this association already exists between an actor and a movie
        existing_association = actor_movie_association.query.filter_by(
            actor_id=actor_id, movie_id=movie_id
        ).first()
        if existing_association:
            return jsonify({'message': 'This association already exists'}), 400

        # Create a new association that an actor will actor in a movie.
        new_association = actor_movie_association(
            actor_id=actor_id, movie_id=movie_id)
        db.session.add(new_association)

        db.session.commit()
        return jsonify(
            {'message': 'Actor successfully assigned to movie'}), 200
    except IntegrityError:
        db.session.rollback()
        abort(400,
              description=
              "Invalid data or violation of database integrity constraints"
        )
    except Exception as e:
        db.session.rollback()
        abort(500, description=str(e))


'''
@COMPLETED_4
API Architecture and Testing

CRITERIA:
- Structure endpoints to respond to four HTTP methods, 
  including error handling.

MEETS SPECIFICATIONS:
- Utilize the @app.errorhandler decorator to format error responses 
  as JSON objects for at least four different status codes.
'''


def my_errorhandler(status_code, message):
    response = jsonify({
        "success": False,
        "error": status_code,
        "message": message
    })
    response.status_code = status_code
    return response


@app.errorhandler(401)
def unauthorized(error):
    return my_errorhandler(401, "Unauthorized")


@app.errorhandler(403)
def forbidden(error):
    return my_errorhandler(403, "Forbidden")


@app.errorhandler(404)
def not_found(error):
    return my_errorhandler(404, "Not Found")


@app.errorhandler(422)
def unprocessable(error):
    return my_errorhandler(422, "Unprocessable Entity")


if __name__ == '__main__':
    app.run(debug=True)
