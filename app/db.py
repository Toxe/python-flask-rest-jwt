from flask import json
from app.models import Ship, User, ship_schema, user_schema


class Database:
    def __init__(self, app=None):
        self.app = app
        self.ships = []
        self.users = []

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.teardown_appcontext(self.teardown)
        with open("data.json") as fp:
            data = json.load(fp)
            self.ships = ship_schema.load(data["ships"], many=True)
            self.users = user_schema.load(data["users"], many=True)

    def teardown(self, exception):
        pass

    def all_ships(self):
        return self.ships

    def all_users(self):
        return self.users

    def get_ship(self, id):
        lst = list(filter(lambda s: s.id == id, self.ships))
        if len(lst) != 1:
            return None
        return lst[0]

    def get_user(self, id):
        lst = list(filter(lambda u: u.id == id, self.users))
        if len(lst) != 1:
            return None
        return lst[0]

    def get_user_by_name(self, name):
        lst = list(filter(lambda u: u.name == name, self.users))
        if len(lst) != 1:
            return None
        return lst[0]

    def get_next_ship_id(self, ships):
        if len(ships) == 0:
            return 1
        return max([s.id for s in ships]) + 1

    def get_next_user_id(self, users):
        if len(users) == 0:
            return 1
        return max([s.id for s in users]) + 1

    def add_ship(self, ship):
        if ship is None or ship.id != 0:
            return None
        ship.id = self.get_next_ship_id(self.ships)
        self.ships.append(ship)
        return ship

    def add_user(self, user):
        if user is None or user.id != 0:
            return None
        user.id = self.get_next_user_id(self.users)
        self.users.append(user)
        return user

    def update_ship(self, ship):
        if ship is None or ship.id <= 0:
            return False
        for key, s in enumerate(self.ships):
            if s.id == ship.id:
                self.ships[key] = ship
                return True
        return False

    def update_user(self, user):
        if user is None or user.id <= 0:
            return False
        for key, s in enumerate(self.users):
            if s.id == user.id:
                self.users[key] = user
                return True
        return False

    def delete_ship(self, id):
        if id <= 0:
            return False
        for key, s in enumerate(self.ships):
            if s.id == id:
                del self.ships[key]
                return True
        return False

    def delete_user(self, id):
        if id <= 0:
            return False
        for key, s in enumerate(self.users):
            if s.id == id:
                del self.users[key]
                return True
        return False
