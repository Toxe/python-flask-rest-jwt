# A (very) basic Flask REST API example

## Dependencies

- Python 3
- Flask
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
$ flask routes
Endpoint       Methods  Rule
-------------  -------  -----------------------
api.get_ship   GET      /api/ships/<int:id>
api.get_ships  GET      /api/ships
api.get_user   GET      /api/users/<int:id>
api.get_users  GET      /api/users
static         GET      /static/<path:filename>
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

## Examples

#### Query all ships

```
$ curl http://localhost:5000/api/ships
```

```json
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
]
```
