from flask import jsonify
from app.api import bp
from app.models import list_ships, find_ship, ship_schema
from app.errors import error_response


@bp.route("/ships", methods=["GET"])
def get_ships():
    return jsonify(ship_schema.dump(list_ships(), many=True))


@bp.route("/ships/<int:id>", methods=["GET"])
def get_ship(id):
    ship = find_ship(id)
    if ship is None:
        return error_response(404)
    return jsonify(ship_schema.dump(ship))
