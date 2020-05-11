from flask import jsonify, request, url_for
from app.api import bp
from app.models import list_ships, find_ship, ship_schema, add_new_ship
from app.errors import error_response
from marshmallow import ValidationError


@bp.route("/ships", methods=["GET"])
def get_ships():
    return jsonify(ship_schema.dump(list_ships(), many=True))


@bp.route("/ships/<int:id>", methods=["GET"])
def get_ship(id):
    ship = find_ship(id)
    if ship is None:
        return error_response(404)
    return jsonify(ship_schema.dump(ship))


@bp.route("/ships", methods=["POST"])
def create_ship():
    try:
        ship = ship_schema.loads(request.data)
    except ValidationError as err:
        return error_response(400, err.messages)
    ship = add_new_ship(ship)
    if ship is None:
        return error_response(400)
    response = jsonify(ship_schema.dump(ship))
    response.status_code = 201
    response.headers["Location"] = url_for("api.get_ship", id=ship.id)
    return response
