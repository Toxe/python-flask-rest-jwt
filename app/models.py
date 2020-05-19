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
    id = fields.Integer(validate=validate.Range(min=1), missing=0)
    name = fields.Str(required=True, validate=validate.Length(min=2))
    password = fields.Str(required=True, validate=validate.Length(min=4), load_only=True)

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)


user_schema = UserSchema()
ship_schema = ShipSchema()
