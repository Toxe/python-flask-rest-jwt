from flask import json
from marshmallow import Schema, fields, post_load, validate


class Ship:
    def __init__(self, id, affiliation, category, crew, length, manufacturer, model, ship_class, roles):
        self.id = id
        self.affiliation = affiliation
        self.category = category
        self.crew = crew
        self.length = length
        self.manufacturer = manufacturer
        self.model = model
        self.ship_class = ship_class
        self.roles = roles
    def __repr__(self):
        return "<Ship({})>".format(self.model)


class ShipSchema(Schema):
    id = fields.Integer(validate=validate.Range(min=1), missing=0)
    affiliation = fields.Str(required=True)
    category = fields.Str(required=True)
    crew = fields.Integer(required=True, validate=validate.Range(min=1))
    length = fields.Integer(required=True, validate=validate.Range(min=1))
    manufacturer = fields.Str(required=True)
    model = fields.Str(required=True)
    ship_class = fields.Str(required=True)
    roles = fields.List(fields.Str(), required=True)

    @post_load
    def make_ship(self, data, **kwargs):
        return Ship(**data)


class User:
    def __init__(self, id, name, password):
        self.id = id
        self.name = name
        self.password = password
    def __repr__(self):
        return "<User({})>".format(self.name)


class UserSchema(Schema):
    id = fields.Integer(validate=validate.Range(min=1))
    name = fields.Str()
    password = fields.Str(load_only=True)

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)


user_schema = UserSchema()
ship_schema = ShipSchema()

users = []
ships = []

with open("data.json") as fp:
    data = json.load(fp)
    users = user_schema.load(data["users"], many=True)
    ships = ship_schema.load(data["ships"], many=True)


def list_ships():
    return ships


def find_ship(id):
    lst = list(filter(lambda s: s.id == id, ships))
    if len(lst) != 1:
        return None
    return lst[0]


def get_next_ship_id(ships):
    if len(ships) == 0:
        return 1
    return max([s.id for s in ships]) + 1


def add_new_ship(ship):
    if ship is None or ship.id != 0:
        return None
    ship.id = get_next_ship_id(ships)
    ships.append(ship)
    return ship


def replace_existing_ship(ship):
    if ship is None or ship.id <= 0:
        return False
    for key, s in enumerate(ships):
        if s.id == ship.id:
            ships[key] = ship
            break
    return True


def list_users():
    return users


def find_user(id):
    lst = list(filter(lambda u: u.id == id, users))
    if len(lst) != 1:
        return None
    return lst[0]
