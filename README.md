# A (very) basic Flask REST API example using JWT Authentication

This is a simple Python REST API server using Flask and JWT. It **does not** use a database or other persistent storage, instead it reads its data on startup from `data.json` and provides some simple database functions for data manipulation and queries. All changes are lost on server shutdown.

The JWT authentication supports access and refresh tokens.

## Dependencies

- Python 3
- Flask
- Flask-JWT-Extended
- Marshmallow
- python-dotenv
- pylint-flask
- pytest

## Configuration

### Flask

#### `.flaskenv` for development and debugging

```ini
FLASK_APP=main
FLASK_ENV=development
```

### Visual Studio Code

#### `.vscode/settings.json`

```json
{
    "python.linting.pylintArgs": [
        "--load-plugins",
        "pylint-flask"
    ]
}
```

## Example data

Example user and ship data is stored in `data.json`.

## Routes

```
$ flask routes --sort rule
Endpoint         Methods  Rule
---------------  -------  -----------------------
api.get_ships    GET      /api/ships
api.create_ship  POST     /api/ships
api.get_ship     GET      /api/ships/<int:id>
api.update_ship  PUT      /api/ships/<int:id>
api.delete_ship  DELETE   /api/ships/<int:id>
api.get_users    GET      /api/users
api.create_user  POST     /api/users
api.get_user     GET      /api/users/<int:id>
api.update_user  PUT      /api/users/<int:id>
api.delete_user  DELETE   /api/users/<int:id>
auth.login       POST     /auth/login
auth.refresh     POST     /auth/refresh
static           GET      /static/<path:filename>
```

## Running (development version)

```
flask run
```

## Tests

Run either of:

```
pytest
```

```
python3 -m pytest
```

## REST API

### Authentication

#### `POST` `/auth/login`: Login

```
$ curl http://localhost:5000/auth/login -X POST -d '{"username":"user", "password":"password"}' -H "Content-Type: application/json"
```

```
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1ODk1MzgwMjYsIm5iZiI6MTU4OTUzODAyNiwianRpIjoiNTM5YzY2ZDUtZWI1My00YzBkLTk4N2MtYzg4OTg2ZDUwZDY1IiwiZXhwIjoxNTg5NTM4OTI2LCJpZGVudGl0eSI6MSwiZnJlc2giOmZhbHNlLCJ0eXBlIjoiYWNjZXNzIn0.SGZW44ceJxwAA5YNcqblkUxDvwZdk0BK9V4ITWedGAs",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1ODk1Mzg0NzMsIm5iZiI6MTU4OTUzODQ3MywianRpIjoiZDE0YmY3Y2MtYjBmMi00N2JlLThjMjktNDcwY2RiYTQ2YzQ4IiwiZXhwIjoxNTkyMTMwNDczLCJpZGVudGl0eSI6MSwidHlwZSI6InJlZnJlc2gifQ.k2-uByI7RbIDTz2sWPhK05oxgfPrr-WVO91osWFpb5A"
}
```

#### `POST` `/auth/refresh`: Refresh access token

```
$ curl http://localhost:5000/auth/refresh -X POST -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1ODk1Mzg0NzMsIm5iZiI6MTU4OTUzODQ3MywianRpIjoiZDE0YmY3Y2MtYjBmMi00N2JlLThjMjktNDcwY2RiYTQ2YzQ4IiwiZXhwIjoxNTkyMTMwNDczLCJpZGVudGl0eSI6MSwidHlwZSI6InJlZnJlc2gifQ.k2-uByI7RbIDTz2sWPhK05oxgfPrr-WVO91osWFpb5A"
```

```
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1ODk1Mzg3NTQsIm5iZiI6MTU4OTUzODc1NCwianRpIjoiOGU4N2I2NWItZTIyOC00ZTk3LWJkZjMtNjZlZDBlYjIzOTllIiwiZXhwIjoxNTg5NTM5NjU0LCJpZGVudGl0eSI6MSwiZnJlc2giOmZhbHNlLCJ0eXBlIjoiYWNjZXNzIn0.pp85jfsbu5LtMlBaMEtrUcFZtgAdu0Vm_WaNsDPUQ-0"
}
```

### Users

#### `GET` `/api/users`: List all users

This will note return stored passwords.

```
$ curl http://localhost:5000/api/users
```

```
[
  {
    "id": 1,
    "name": "user"
  },
  {
    "id": 2,
    "name": "guest"
  }
]
```

#### `GET` `/api/users/<id>`: Query single user

This will not return the user password.

```
$ curl http://localhost:5000/api/users/1
```

```
{
  "id": 1,
  "name": "user"
}
```

#### `POST` `/api/users`: Create new user

```
$ curl http://localhost:5000/api/users -X POST -d '{"name":"new user", "password":"secret"}' -H "Content-Type: application/json"
```

```
{
  "id": 3,
  "name": "new user"
}
```

#### `PUT` `/api/users/<id>`: Update user data

Login required and can only change own data.

```
$ curl http://localhost:5000/api/users/3 -X PUT -d '{"name":"fancy new name", "password":"more secret"}' -H "Content-Type: application/json" -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1ODk1Mzk1NjUsIm5iZiI6MTU4OTUzOTU2NSwianRpIjoiOTg4MzgzM2UtYTA2Yi00OWVjLTlmNDYtMWY3OGFkMzJhOTdhIiwiZXhwIjoxNTg5NTQwNDY1LCJpZGVudGl0eSI6MywiZnJlc2giOmZhbHNlLCJ0eXBlIjoiYWNjZXNzIn0._5zSHBsN1jUvaLxkSaC1lW6aRemm_1fGvp-Nufb2028"
```

```
{
  "id": 3,
  "name": "fancy new name"
}
```

#### `DELETE` `/api/users/<id>`: Delete user

Login required and can only delete the current user.

```
$ curl http://localhost:5000/api/users/3 -X DELETE -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1ODk1Mzk1NjUsIm5iZiI6MTU4OTUzOTU2NSwianRpIjoiOTg4MzgzM2UtYTA2Yi00OWVjLTlmNDYtMWY3OGFkMzJhOTdhIiwiZXhwIjoxNTg5NTQwNDY1LCJpZGVudGl0eSI6MywiZnJlc2giOmZhbHNlLCJ0eXBlIjoiYWNjZXNzIn0._5zSHBsN1jUvaLxkSaC1lW6aRemm_1fGvp-Nufb2028"
```

### Ships

#### `GET` `/api/ships`: List all ships

```
$ curl http://localhost:5000/api/ships
```

```
[
  {
    "affiliation": "Rebel Alliance",
    "category": "Starfighters",
    "crew": 1,
    "id": 1,
    "length": 13,
    "manufacturer": "Incom Corporation",
    "model": "T-65 X-Wing",
    "roles": [
      "Space Superiority Starfighter",
      "Escort"
    ],
    "ship_class": "Starfighter"
  },
  [...]
```

#### `GET` `/api/ship/<id>`: Query single ship

```
$ curl http://localhost:5000/api/ships/2
```

```
{
  "affiliation": "Empire",
  "category": "Starfighters",
  "crew": 1,
  "id": 2,
  "length": 7,
  "manufacturer": "Sienar Fleet Systems",
  "model": "TIE/LN Starfighter",
  "roles": [
    "Space Superiority Starfighter"
  ],
  "ship_class": "Starfighter"
}
```

#### `POST` `/api/ship`: Create new ship

Login required.

```
$ curl http://localhost:5000/api/ships -X POST -d '{"ship_class":"Star Destroyer", "model":"Imperial I-class Star Destroyer", "affiliation":"Empire", "category":"Capital Ships", "crew":37085, "length":1600, "manufacturer":"Kuat Drive Yards", "roles":["Destroyer","Carrier","Military Transport","Command Ship"]}' -H "Content-Type: application/json" -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1ODk1NDY2NzEsIm5iZiI6MTU4OTU0NjY3MSwianRpIjoiMzhiOWZlZjUtMDEwOC00ODljLTljNjYtY2Q2YzZkMGViNWI3IiwiZXhwIjoxNTg5NTQ3NTcxLCJpZGVudGl0eSI6MSwiZnJlc2giOmZhbHNlLCJ0eXBlIjoiYWNjZXNzIn0.rbCRtuhRN4__IuR7WvYMQY5Q6goxm6PyIHcz0xE-8DQ"
```

```
{
  "affiliation": "Empire",
  "category": "Capital Ships",
  "crew": 37085,
  "id": 16,
  "length": 1600,
  "manufacturer": "Kuat Drive Yards",
  "model": "Imperial I-class Star Destroyer",
  "roles": [
    "Destroyer",
    "Carrier",
    "Military Transport",
    "Command Ship"
  ],
  "ship_class": "Star Destroyer"
}
```

#### `PUT` `/api/ship/<id>`: Update ship

Login required.

```
$ curl http://localhost:5000/api/ships/16 -X PUT -d '{"ship_class":"Star Destroyer", "model":"Imperial II-class Star Destroyer", "affiliation":"Empire", "category":"Capital Ships", "crew":37050, "length":1600, "manufacturer":"Kuat Drive Yards", "roles":["Destroyer","Carrier","Military Transport","Command Ship"]}' -H "Content-Type: application/json" -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1ODk1NDY2NzEsIm5iZiI6MTU4OTU0NjY3MSwianRpIjoiMzhiOWZlZjUtMDEwOC00ODljLTljNjYtY2Q2YzZkMGViNWI3IiwiZXhwIjoxNTg5NTQ3NTcxLCJpZGVudGl0eSI6MSwiZnJlc2giOmZhbHNlLCJ0eXBlIjoiYWNjZXNzIn0.rbCRtuhRN4__IuR7WvYMQY5Q6goxm6PyIHcz0xE-8DQ"
```

```
{
  "affiliation": "Empire",
  "category": "Capital Ships",
  "crew": 37050,
  "id": 16,
  "length": 1600,
  "manufacturer": "Kuat Drive Yards",
  "model": "Imperial II-class Star Destroyer",
  "roles": [
    "Destroyer",
    "Carrier",
    "Military Transport",
    "Command Ship"
  ],
  "ship_class": "Star Destroyer"
}
```

#### `DELETE` `/api/ship/<id>`: Delete ship

Login required.

```
$ curl -i http://localhost:5000/api/ships/16 -X DELETE -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1ODk1NDY2NzEsIm5iZiI6MTU4OTU0NjY3MSwianRpIjoiMzhiOWZlZjUtMDEwOC00ODljLTljNjYtY2Q2YzZkMGViNWI3IiwiZXhwIjoxNTg5NTQ3NTcxLCJpZGVudGl0eSI6MSwiZnJlc2giOmZhbHNlLCJ0eXBlIjoiYWNjZXNzIn0.rbCRtuhRN4__IuR7WvYMQY5Q6goxm6PyIHcz0xE-8DQ"
```

```
HTTP/1.0 204 NO CONTENT
Content-Type: text/html; charset=utf-8
Server: Werkzeug/1.0.1 Python/3.8.2
Date: Fri, 15 May 2020 12:52:05 GMT
```
