from flask import jsonify
from app.api import bp
from app.models import list_users, find_user, user_schema
from app.errors import error_response


@bp.route("/users", methods=["GET"])
def get_users():
    return jsonify(user_schema.dump(list_users(), many=True))


@bp.route("/users/<int:id>", methods=["GET"])
def get_user(id):
    user = find_user(id)
    if user is None:
        return error_response(404)
    return jsonify(user_schema.dump(user))
