from flask import jsonify
from app.api import bp
from app.models import list_users, find_user


@bp.route("/users", methods=["GET"])
def get_users():
    return jsonify(list_users())


@bp.route("/users/<int:id>", methods=["GET"])
def get_user(id):
    return jsonify(find_user(id))
