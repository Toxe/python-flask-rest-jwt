from flask import jsonify, request, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.api import bp
from app.models import user_schema
from app.errors import error_response
from marshmallow import ValidationError


@bp.route("/users", methods=["GET"])
def get_users():
    return jsonify(user_schema.dump(db.all_users(), many=True))


@bp.route("/users/<int:id>", methods=["GET"])
def get_user(id):
    user = db.get_user(id)
    if user is None:
        return error_response(404)
    return jsonify(user_schema.dump(user))


@bp.route("/users", methods=["POST"])
def create_user():
    try:
        user = user_schema.loads(request.data)
    except ValidationError as err:
        return error_response(400, err.messages)
    user = db.add_user(user)
    if user is None:
        return error_response(400)
    response = jsonify(user_schema.dump(user))
    response.status_code = 201
    response.headers["Location"] = url_for("api.get_user", id=user.id)
    return response


@bp.route("/users/<int:id>", methods=["PUT"])
@jwt_required
def update_user(id):
    if id != get_jwt_identity():
        return error_response(403)
    try:
        user = user_schema.loads(request.data)
    except ValidationError as err:
        return error_response(400, err.messages)
    if db.get_user(id) is None:
        return error_response(404)
    # "id" in request data is optional
    if user.id == 0:
        user.id = id
    # if "id" was provided in request data then it has to match the resource id
    if user.id != id:
        return error_response(400, "Request data id has to match resource id.")
    if not db.update_user(user):
        return error_response(400)
    response = jsonify(user_schema.dump(user))
    return response


@bp.route("/users/<int:id>", methods=["DELETE"])
@jwt_required
def delete_user(id):
    if id != get_jwt_identity():
        return error_response(403)
    if db.get_user(id) is None:
        return error_response(404)
    if db.delete_user(id) is False:
        return error_response(400)
    return "", 204
