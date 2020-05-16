# A (very) basic Flask REST API example using JWT Authentication

This is a simple Python REST API server using Flask and JWT (JSON Web Tokens). It **does not** use a database or other persistent storage, instead it reads its data on startup from `data.json` and provides some simple database functions for data manipulation and queries. All changes are lost on server shutdown.

The JWT authentication supports access and refresh tokens and token revoking by using an in-memory blacklist.

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
Endpoint                   Methods  Rule
-------------------------  -------  -----------------------
api.get_ships              GET      /api/ships
api.create_ship            POST     /api/ships
api.get_ship               GET      /api/ships/<int:id>
api.update_ship            PUT      /api/ships/<int:id>
api.delete_ship            DELETE   /api/ships/<int:id>
api.get_users              GET      /api/users
api.create_user            POST     /api/users
api.get_user               GET      /api/users/<int:id>
api.update_user            PUT      /api/users/<int:id>
api.delete_user            DELETE   /api/users/<int:id>
auth.login                 POST     /auth/login
auth.logout_access_token   DELETE   /auth/logout
auth.logout_refresh_token  DELETE   /auth/logout2
auth.refresh               POST     /auth/refresh
static                     GET      /static/<path:filename>
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

##### `POST` `/auth/login`: Login

```
$ curl -i http://localhost:5000/auth/login -X POST -d '{"username":"user", "password":"password"}' -H "Content-Type: application/json"
```

```
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 568
Server: Werkzeug/1.0.1 Python/3.8.2
Date: Fri, 15 May 2020 12:56:25 GMT

{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1ODk1NDczODUsIm5iZiI6MTU4OTU0NzM4NSwianRpIjoiMDE5NmJkMjAtZGMxOC00NTI0LWEzM2UtNWEzYTZiNGMxZTQ2IiwiZXhwIjoxNTg5NTQ4Mjg1LCJpZGVudGl0eSI6MSwiZnJlc2giOmZhbHNlLCJ0eXBlIjoiYWNjZXNzIn0.7Jeg7_Yv22vzKAM6ZfOgp5JQjEGAJLWB_k6qDpfx5HU",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1ODk1NDczODUsIm5iZiI6MTU4OTU0NzM4NSwianRpIjoiMmFhZDQxNTEtMDFmNi00YzM4LWFiYjctZWE2M2YyYjhlMjE3IiwiZXhwIjoxNTkyMTM5Mzg1LCJpZGVudGl0eSI6MSwidHlwZSI6InJlZnJlc2gifQ.SazEtt-odtprlo2eD8XiE90chQm87PfYt7UyMj5rvVk"
}
```

##### `POST` `/auth/refresh`: Refresh access token

```
$ curl -i http://localhost:5000/auth/refresh -X POST -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1ODk1NDczODUsIm5iZiI6MTU4OTU0NzM4NSwianRpIjoiMmFhZDQxNTEtMDFmNi00YzM4LWFiYjctZWE2M2YyYjhlMjE3IiwiZXhwIjoxNTkyMTM5Mzg1LCJpZGVudGl0eSI6MSwidHlwZSI6InJlZnJlc2gifQ.SazEtt-odtprlo2eD8XiE90chQm87PfYt7UyMj5rvVk"
```

```
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 293
Server: Werkzeug/1.0.1 Python/3.8.2
Date: Fri, 15 May 2020 12:57:56 GMT

{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1ODk1NDc0NzYsIm5iZiI6MTU4OTU0NzQ3NiwianRpIjoiNWE1Mzg0MGUtYjZmNS00ZTFkLTg3MGMtYzViNDliYmVkOGQzIiwiZXhwIjoxNTg5NTQ4Mzc2LCJpZGVudGl0eSI6MSwiZnJlc2giOmZhbHNlLCJ0eXBlIjoiYWNjZXNzIn0.4j4jonxmnAP1hFkJSCryIkKWOrMtJU02BqUIBUukpKA"
}
```

##### `DELETE` `/auth/logout`: Logout and revoke access token

```
$ curl -i http://localhost:5000/auth/logout -X DELETE -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1ODk2MTc4NzIsIm5iZiI6MTU4OTYxNzg3MiwianRpIjoiYzUwNDlkMmEtZWIyZS00M2I1LWIzNjgtMTJjYWFiMjA3ZTJjIiwiZXhwIjoxNTg5NjE4NzcyLCJpZGVudGl0eSI6MSwiZnJlc2giOmZhbHNlLCJ0eXBlIjoiYWNjZXNzIn0.XoQtFc-a9ak4ON8TQ6rKYzz8IZWlYCeTZph4fomX-tw"
```

```
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 44
Server: Werkzeug/1.0.1 Python/3.8.2
Date: Sat, 16 May 2020 08:32:18 GMT

{
  "message": "Successfully logged out."
}
```

##### `DELETE` `/auth/logout2`: Logout and revoke refresh token

```
$ curl -i http://localhost:5000/auth/logout2 -X DELETE -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1ODk2MTc4NzIsIm5iZiI6MTU4OTYxNzg3MiwianRpIjoiYzA2YTA2NWEtMmJiYS00ZTJlLTliZTctY2Y0YWM4MWUwZDA2IiwiZXhwIjoxNTkyMjA5ODcyLCJpZGVudGl0eSI6MSwidHlwZSI6InJlZnJlc2gifQ.XsZ1cHcFhA60k4z87-bbuHBkRmWD6hKAXifzFq2NjOw"
```

```
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 44
Server: Werkzeug/1.0.1 Python/3.8.2
Date: Sat, 16 May 2020 08:34:18 GMT

{
  "message": "Successfully logged out."
}
```

### Users

##### `GET` `/api/users`: List all users

This will not return stored passwords.

```
$ curl -i http://localhost:5000/api/users
```

```
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 89
Server: Werkzeug/1.0.1 Python/3.8.2
Date: Fri, 15 May 2020 12:58:30 GMT

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

##### `GET` `/api/users/<id>`: Query single user

This will not return the user password.

```
$ curl -i http://localhost:5000/api/users/1
```

```
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 33
Server: Werkzeug/1.0.1 Python/3.8.2
Date: Fri, 15 May 2020 12:58:52 GMT

{
  "id": 1,
  "name": "user"
}
```

##### `POST` `/api/users`: Create new user

```
$ curl -i http://localhost:5000/api/users -X POST -d '{"name":"new user", "password":"secret"}' -H "Content-Type: application/json"
```

```
HTTP/1.0 201 CREATED
Content-Type: application/json
Content-Length: 37
Location: http://localhost:5000/api/users/3
Server: Werkzeug/1.0.1 Python/3.8.2
Date: Fri, 15 May 2020 12:59:19 GMT

{
  "id": 3,
  "name": "new user"
}
```

##### `PUT` `/api/users/<id>`: Update user data

Login required and can only change own data.

```
$ curl -i http://localhost:5000/api/users/3 -X PUT -d '{"name":"fancy new name", "password":"more secret"}' -H "Content-Type: application/json" -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1ODk1NDc3MDYsIm5iZiI6MTU4OTU0NzcwNiwianRpIjoiOTJjYTdhMTItY2Q4Yi00ZWJjLThlMWEtMjU1N2EwMGYwY2Y0IiwiZXhwIjoxNTg5NTQ4NjA2LCJpZGVudGl0eSI6MywiZnJlc2giOmZhbHNlLCJ0eXBlIjoiYWNjZXNzIn0.FLFRjkTAzpeT-ZOUsZmWegy5cn-EHM8EeC3Tskuu4Uc"
```

```
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 43
Server: Werkzeug/1.0.1 Python/3.8.2
Date: Fri, 15 May 2020 13:02:09 GMT

{
  "id": 3,
  "name": "fancy new name"
}
```

##### `DELETE` `/api/users/<id>`: Delete user

Login required and can only delete the current user.

```
$ curl -i http://localhost:5000/api/users/3 -X DELETE -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1ODk1NDc3MDYsIm5iZiI6MTU4OTU0NzcwNiwianRpIjoiOTJjYTdhMTItY2Q4Yi00ZWJjLThlMWEtMjU1N2EwMGYwY2Y0IiwiZXhwIjoxNTg5NTQ4NjA2LCJpZGVudGl0eSI6MywiZnJlc2giOmZhbHNlLCJ0eXBlIjoiYWNjZXNzIn0.FLFRjkTAzpeT-ZOUsZmWegy5cn-EHM8EeC3Tskuu4Uc"
```

```
HTTP/1.0 204 NO CONTENT
Content-Type: text/html; charset=utf-8
Server: Werkzeug/1.0.1 Python/3.8.2
Date: Fri, 15 May 2020 13:02:30 GMT
```

### Ships

##### `GET` `/api/ships`: List all ships

```
$ curl -i http://localhost:5000/api/ships
```

```
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 4984
Server: Werkzeug/1.0.1 Python/3.8.2
Date: Fri, 15 May 2020 13:03:08 GMT

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
  {"id": 2, ...},
  {"id": 3, ...},
  {"id": 4, ...},
  {"id": 5, ...},
  {"id": 6, ...},
  {"id": 7, ...},
  {"id": 8, ...},
  {"id": 9, ...},
  {"id": 10, ...},
  {"id": 11, ...},
  {"id": 12, ...},
  {"id": 13, ...},
  {"id": 14, ...},
  {"id": 15, ...}
]
```

##### `GET` `/api/ship/<id>`: Query single ship

```
$ curl -i http://localhost:5000/api/ships/2
```

```
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 267
Server: Werkzeug/1.0.1 Python/3.8.2
Date: Fri, 15 May 2020 13:06:32 GMT

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

##### `POST` `/api/ship`: Create new ship

Login required.

```
$ curl -i http://localhost:5000/api/ships -X POST -d '{"ship_class":"Star Destroyer", "model":"Imperial I-class Star Destroyer", "affiliation":"Empire", "category":"Capital Ships", "crew":37085, "length":1600, "manufacturer":"Kuat Drive Yards", "roles":["Destroyer","Carrier","Military Transport","Command Ship"]}' -H "Content-Type: application/json" -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1ODk1NDc0NzYsIm5iZiI6MTU4OTU0NzQ3NiwianRpIjoiNWE1Mzg0MGUtYjZmNS00ZTFkLTg3MGMtYzViNDliYmVkOGQzIiwiZXhwIjoxNTg5NTQ4Mzc2LCJpZGVudGl0eSI6MSwiZnJlc2giOmZhbHNlLCJ0eXBlIjoiYWNjZXNzIn0.4j4jonxmnAP1hFkJSCryIkKWOrMtJU02BqUIBUukpKA"
```

```
HTTP/1.0 201 CREATED
Content-Type: application/json
Content-Length: 332
Location: http://localhost:5000/api/ships/16
Server: Werkzeug/1.0.1 Python/3.8.2
Date: Fri, 15 May 2020 13:07:38 GMT

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

##### `PUT` `/api/ship/<id>`: Update ship

Login required.

```
$ curl -i http://localhost:5000/api/ships/16 -X PUT -d '{"ship_class":"Star Destroyer", "model":"Imperial II-class Star Destroyer", "affiliation":"Empire", "category":"Capital Ships", "crew":37050, "length":1600, "manufacturer":"Kuat Drive Yards", "roles":["Destroyer","Carrier","Military Transport","Command Ship"]}' -H "Content-Type: application/json" -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1ODk1NDc0NzYsIm5iZiI6MTU4OTU0NzQ3NiwianRpIjoiNWE1Mzg0MGUtYjZmNS00ZTFkLTg3MGMtYzViNDliYmVkOGQzIiwiZXhwIjoxNTg5NTQ4Mzc2LCJpZGVudGl0eSI6MSwiZnJlc2giOmZhbHNlLCJ0eXBlIjoiYWNjZXNzIn0.4j4jonxmnAP1hFkJSCryIkKWOrMtJU02BqUIBUukpKA"
```

```
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 333
Server: Werkzeug/1.0.1 Python/3.8.2
Date: Fri, 15 May 2020 13:07:56 GMT

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

##### `DELETE` `/api/ship/<id>`: Delete ship

Login required.

```
$ curl -i -i http://localhost:5000/api/ships/16 -X DELETE -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1ODk1NDc0NzYsIm5iZiI6MTU4OTU0NzQ3NiwianRpIjoiNWE1Mzg0MGUtYjZmNS00ZTFkLTg3MGMtYzViNDliYmVkOGQzIiwiZXhwIjoxNTg5NTQ4Mzc2LCJpZGVudGl0eSI6MSwiZnJlc2giOmZhbHNlLCJ0eXBlIjoiYWNjZXNzIn0.4j4jonxmnAP1hFkJSCryIkKWOrMtJU02BqUIBUukpKA"
```

```
HTTP/1.0 204 NO CONTENT
Content-Type: text/html; charset=utf-8
Server: Werkzeug/1.0.1 Python/3.8.2
Date: Fri, 15 May 2020 13:08:25 GMT
```
