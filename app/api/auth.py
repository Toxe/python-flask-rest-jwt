from flask import jsonify, request
from flask_jwt_extended import create_access_token, decode_token
from app import db
from app.api import bp
from app.errors import error_response


@bp.route("/login", methods=["POST"])
def login():
    if not request.is_json:
        return error_response(400)

    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return error_response(400, "Username or password missing.")

    user = db.get_user_by_name(username)

    if not user or user.password != password:
        return error_response(401, "Username or password invalid.")

    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token)
