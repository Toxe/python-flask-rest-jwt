from flask import json
from marshmallow import Schema, fields, post_load, validate, ValidationError


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
    id = fields.Integer(validate=validate.Range(min=1))
    affiliation = fields.Str()
    category = fields.Str()
    crew = fields.Integer(validate=validate.Range(min=1))
    length = fields.Integer(validate=validate.Range(min=1))
    manufacturer = fields.Str()
    model = fields.Str()
    ship_class = fields.Str()
    roles = fields.List(fields.Str())

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


def list_users():
    return users


def find_user(id):
    lst = list(filter(lambda u: u.id == id, users))
    if len(lst) != 1:
        return None
    return lst[0]
