from copy import deepcopy
from flask import json


users = []
ships = []

with open("data.json") as fp:
    data = json.load(fp)
    users = data["users"]
    ships = data["ships"]


def list_ships():
    return ships


def find_ship(id):
    lst = list(filter(lambda s: s["id"] == id, ships))
    if len(lst) != 1:
        return None
    return lst[0]


def remove_password(user_orig):
    user_new = dict(user_orig)
    del user_new["password"]
    return user_new


def list_users():
    return list(map(remove_password, users))


def find_user(id):
    lst = list(filter(lambda u: u["id"] == id, users))
    if len(lst) != 1:
        return None
    return remove_password(lst[0])
