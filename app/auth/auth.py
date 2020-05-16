from flask import jsonify, request
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_required, jwt_refresh_token_required,
    get_jwt_identity, get_raw_jwt
)
from app import db, jwt
from app.auth import bp
from app.errors import error_response


blacklist = set()


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token["jti"] in blacklist


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
    refresh_token = create_refresh_token(identity=user.id)
    return jsonify(access_token=access_token, refresh_token=refresh_token)


@bp.route("/refresh", methods=["POST"])
@jwt_refresh_token_required
def refresh():
    user = db.get_user(get_jwt_identity())
    if not user:
        return error_response(401, "Unknown user.")
    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token)


# revoke current access token
@bp.route("/logout", methods=["DELETE"])
@jwt_required
def logout_access_token():
    blacklist.add(get_raw_jwt()["jti"])
    return jsonify(message="Successfully logged out.")


# revoke current refresh token
@bp.route("/logout2", methods=["DELETE"])
@jwt_refresh_token_required
def logout_refresh_token():
    blacklist.add(get_raw_jwt()["jti"])
    return jsonify(message="Successfully logged out.")
