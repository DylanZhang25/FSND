# FSND - Capstone

## Getting Started
### Pre-requisites and Local Development
Users using this project should already have Python 3.11.3 and pip installed on their local machines. Also, this project is built and tested in Windows 11 System.
___
### Project Structure
```
- flask_CastingAgencyModels
	- static
		- css
		- font
		- pictures
		- utils
		- favicon.ico
		- layui.js
	- templates
		- actor_add.html
		- actor_edit.html
		- index.html
		- movie_card.html
		- movies-popup.html
	- .env
	- app.py
	- config.py
	- extensions.py
	- models.py
	- test_CAM.py
	- README.md
	- requirements.txt	
```
___
### Backend Setup and Run
#### 1. Set up Python Virtual Environment
* Open Windows Command Prompt at the same level as the project folder
* In the above location, use python 3.11 to create a virtual environment, named venv (random name, here named venv for convenience), using:
```
C:\Users\your_user_name\AppData\Local\Programs\Python\Python37\python.exe -m venv venv
```
Note: `C:\Users\yourUsername\AppData\Local\Programs\Python\Python311` is the default location where you installed your Python 3.11 on your Windows.
* In the location at the same level as the virtual environment folder, activate the virtual environment in the terminal using:
```
venv\Scripts\activate
```
#### 2. In the virtual environment, clone the GitHub project to local
#### 3. Installing Dependencies
* In the virtual environment, under the project's backend folder, install the dependency using:
```
pip install -r requirements.txt
```
* To avoid package incompatibility, it is possible to update all packages to the latest version through pip. Here is the versions of my packages:
```
Package           Version
----------------- -------
Authlib           1.2.1
blinker           1.6.2
cffi              1.15.1
click             8.1.7
colorama          0.4.6
cryptography      41.0.3
ecdsa             0.18.0
Faker             19.3.0
Flask             2.3.2
Flask-Admin       1.6.1
Flask-SQLAlchemy  3.0.5
greenlet          2.0.2
itsdangerous      2.1.2
Jinja2            3.1.2
MarkupSafe        2.1.3
pip               23.2.1
psycopg2          2.9.7
psycopg2-binary   2.9.7
pyasn1            0.5.0
pycparser         2.21
PyJWT             2.8.0
python-dateutil   2.8.2
python-dotenv     1.0.0
python-jose       3.3.0
rsa               4.9
setuptools        65.5.1
six               1.16.0
SQLAlchemy        2.0.20
typing_extensions 4.7.1
Werkzeug          2.3.7
wheel             0.38.4
WTForms           3.0.1

```
* Using a specific version of the Python interpreter and installed packages in a virtual environment
Create a file named .env in the root directory of the virtual environment (if it does not already exist) and add the following to it:
```
PYTHONPATH=D:\path-to-your-project\venv\Scripts\python.exe
```

#### 4. Run Backend
in the folder of the position of `app.py`, in the terminal run:
```
flask run --debug --reload 
```
___
### Frontend Setup and Run
The frontend of this project is only using JavaScript and Layui, no more additional actions are needed.
___
### Tests
Due to the limitation of Render.com, a free account can create one Postgres Database only. In this case, this project assumes the testing and deployment database are the same one. 
In the backend, users can generate a demo database using the Flask CLI, Movies and Actors data for testing will be added to the database automatically.
```
flask create_a_demo_database_cli
```
To test the endpoints in `app.py`, in the terminal, run the following commands after navigating to the backend folder:
```
python test_flaskr.py
```
However, I suggest users to test endpoints one by one due to the performance issue of Render.com free account, sometimes the Render.com server will not return the query results timely. 
```
python -m unittest test_CAM.CastingAgencyModelsTestCase.test_casting_assistant_get_movies
python -m unittest test_CAM.CastingAgencyModelsTestCase.test_casting_assistant_no_permission_to_get_actors
python -m unittest test_CAM.test_casting_director_get_movies
python -m unittest test_CAM.CastingAgencyModelsTestCase.test_casting_director_get_actors
python -m unittest test_CAM.CastingAgencyModelsTestCase.test_get_actors_functionality_success
python -m unittest test_CAM.CastingAgencyModelsTestCase.test_get_actors_functionality_error
python -m unittest test_CAM.CastingAgencyModelsTestCase.test_add_actor_functionality_success
python -m unittest test_CAM.CastingAgencyModelsTestCase.test_add_actor_functionality_error_missing_field
python -m unittest test_CAM.CastingAgencyModelsTestCase.test_patch_actor_success
python -m unittest test_CAM.CastingAgencyModelsTestCase.test_patch_actor_failure_invalid_id
python -m unittest test_CAM.CastingAgencyModelsTestCase.test_delete_actor_success
python -m unittest test_CAM.CastingAgencyModelsTestCase.test_delete_actor_failure_invalid_id
python -m unittest test_CAM.CastingAgencyModelsTestCase.test_get_movies_success
python -m unittest test_CAM.CastingAgencyModelsTestCase.test_get_movies_non_existent_page
```
___
### API Reference
#### Getting Started
* Base URL: the backend app is hosted at the default, http://127.0.0.1:5000.
* Authentication:
  - Roles
      - CastingAssistant
      - CastingDirector
  - Related Permissions For Each Role:
    - CastingAssistant: 
        'get:movies'
    - CastingDirector: 
      - 'delete:actor',
      - 'get:actors',
      - 'get:movies',
      - 'patch:actor',
      - 'post:actor'
  - Demo access_token for testing
    - Note: each access_token will expire after 24 hours, which is the maximum time length from Auth0.
    - Casting Assistant's access_token: eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InlUd2hiNVdZRmVJdWdBSkM0Q0dleCJ9.eyJjYXN0aW5nYWdlbmN5LXVzZXItZW1haWwiOiJpX2FtX2FfY2FzdGluZ2Fzc2lzdGFudEBnbWFpbC5jb20iLCJpc3MiOiJodHRwczovL2h0NzI1LmF1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NGZlYmM3N2JlNTQ5Yzc0NDA2YzQ5YTciLCJhdWQiOiJjYXN0aW5nYWdlbmN5YXBpcyIsImlhdCI6MTY5NTU1NzAyNCwiZXhwIjoxNjk1NjQzNDI0LCJhenAiOiI1N3UzS3gwaG1xWnVMZ2JwWlY0cjJ2U2haNm9Bb1N6UyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0Om1vdmllcyJdfQ.IWqHeLpEougBBOKb3mqcBwLSXSETy-fUeLoIP7J0ZhFUbbdwZjJtSZXBDrtfI-eV0fgx5B-GcDNL62bJEC-zUyCl7dieYH74Ibvu_ifSCxmrcMP0KP7f4ZkokFvNFDmYf6Pvak15CIE9WsaSfSjFoADmcpQH41X9fH_uX9jnnQSVZSo13sPZpuJ6YPYk9OMH23hPsVykF36DSFNWWlyls9vRIRNhhtJwoaKDJoHzslqyt_ITOEMwU3zARAA3FneI4CX4-PuMSroIUingiRBYv4bUz4D-nl30CFpak5hSowIP9gKEZPw74MsBOOeJ8wRCd9tVLg9rdjB5QvmkdwRbug
    - Casting Director's access_token: eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InlUd2hiNVdZRmVJdWdBSkM0Q0dleCJ9.eyJjYXN0aW5nYWdlbmN5LXVzZXItZW1haWwiOiJpX2FtX2FfY2FzdGluZ2RpcmVjdG9yQGdtYWlsLmNvbSIsImlzcyI6Imh0dHBzOi8vaHQ3MjUuYXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDY0ZmViY2YxYzA5NWM4NzJjYjE5YzhlYyIsImF1ZCI6ImNhc3RpbmdhZ2VuY3lhcGlzIiwiaWF0IjoxNjk1NTU3MDgxLCJleHAiOjE2OTU2NDM0ODEsImF6cCI6IjU3dTNLeDBobXFadUxnYnBaVjRyMnZTaFo2b0FvU3pTIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3IiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9yIiwicG9zdDphY3RvciJdfQ.YkUyo79QdEdKxjLA5Zx_DiSai-HPHGdUXOqmLe4t5GNMFzp4cuXzS-6pmnEeKPaWOinzsk71yOuCrCcuB5mRXUb8dm8fF-zh7gUFP1iATRq2g3nAGhrF9O6m4AzYPEZS8QODwVDx_-EoZwPV4DLJ1Evt6E4OIsXtU38CqG5YDidAK_HwsaMIL_yXYkjYm6SQUj1Z5f89kCXCA4JT8NILBHb8Ahq4DXy-8E8-ZzdPNpaRm0X73cS9Dgj7SadGy8SDntX2pho_nP8S4Jx3wre-Po_cVW4DfccE-EkHUZtHOXS4TLpHyMdnXqNAgB7WF61fv55ZQklPJsNjIoE5bXwu_w
##### Error Handling
Errors are returned as JSON objects following the format below:
```
{
	"success": False,
	"error": status_code,
	"message": message
}
```
When a request fails, the API will return four error types:
* 400
* 403
* 404
* 422

#### Endpoints

`GET '/api/actors'`
* Sample:
	`http://localhost:5000/api/actors`
* General Purpose:
  - the list of actors.You can get it in pages by page number or fuzzy query by actor name.
* Request Arguments:
  - page: int (Optional, indicates the page number of the request, default is 1)
  - name: string (Optional, for fuzzy query based on actor name)
* Response format:
```json
{
  "code": 200,
  "msg": "actor query success",
  "count": 30,
  "data": [
      {
          "id": 1,
          "name": "Mikal Jackson",
          "age": "99",
          "is_time_available": true,
          "create_at": "2023-09-20 23:49:19",
          "update_at": "2023-09-20 23:49:19",
          "movies": []
      }
  ]
}
```
---
`POST '/api/actor'`
* Sample:
	`http://localhost:5000/api/actor`
* General Purpose:
	- Add a new actor.
* Request Authentication:
  - Requires authentication token with 'post:actor' permission.
* Request Body:
```json
{
  "name": "Actor Name",
  "age": 99,
  "is_time_available": false,
  "create_at": "2023-09-20 23:49:19"
}
```
Note: All properties are required.
* Response format:
```json
{
  "code": 201,
  "msg": "Succeeded in adding data",
  "page_number": 3,
  "count": 30
}
```
---
`PATCH '/api/actor/<int:aid>'`
* Sample:
	`http://localhost:5000/api/actor/1`
* General Purpose:
  - Update the information of an actor with the specified ID.
* Path Parameters:
  - aid: int, required, representing the ID of the actor to be patched.
* Request Authentication:
  - Requires authentication token with 'patch:actor' permission.
* Request Body:
```json
{
  "name": "Actor Name",
  "age": "99",
  "is_time_available": true,
  "update_at": "2023-09-20 23:49:19"
}
```
Note: All properties are optional, but at least one should be provided for an update.
* Response format:
```json
{
  "code": 200,
  "msg": "Succeeded in editing data"
}
```
---
`DELETE '/api/actor/int:aid'`
* Sample:
	`http://localhost:5000/api/actor/20`
* General Purpose:
  - Delete the actor identified by the specified ID from the database.
* Path Parameters:
  - aid: int, required, representing the ID of the actor to be deleted.
* Request Authentication:
  - Requires authentication token with 'delete:actor' permission.
* Response Format:
```
{
  "code": 200,
  "msg": "Succeeded in deleting data"
}
```
---
`GET '/api/movies'`
* Sample:
	`http://localhost:5000/api/movies`
* General Purpose:
  - Retrieve a paginated list of movies from the database, including associated actor information and rendered HTML for each movie.
* Query Parameters:
  - page: int, optional, default value is 1, representing the page number to be retrieved.
* Request Authentication:
  - Requires authentication token with 'get:movies' permission.
* Response Format:
```json
{
  "movies": [
    {
      "id": 1,
      "title": "Movie Title",
      "date": "2023-09-24",
      "actors": ["Actor Name"],
      "html": "<div>Rendered HTML for movie</div>"
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 8,
    "total": 100,
    "pages": 13
  }
}
```
---
`POST '/api/assign_actor_to_movie'`
* Sample:
	`http://localhost:5000/api/assign_actor_to_movie'`
* General Purpose:
  - Assign a specified actor to a movie. This creates an association between the actor and the movie in the database.
* Request Authentication:
  - Requires authentication token with 'patch:actor' permission.
* Request Body:
```json
{
  "actor_id": 1,
  "movie_id": 2
}
```
* Response Body:

```json
{
	"code": 200,
	"message": "Actor successfully assigned to movie"
}
```
