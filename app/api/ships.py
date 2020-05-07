from flask import jsonify
from app.api import bp
from app.models import list_ships, find_ship


@bp.route("/ships", methods=["GET"])
def get_ships():
    return jsonify(list_ships())


@bp.route("/ships/<int:id>", methods=["GET"])
def get_ship(id):
    return jsonify(find_ship(id))
