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
    return ships[id - 1]


def list_users():
    return users


def find_user(id):
    return users[id - 1]
