from flask import jsonify
from app import db
from app.api import bp
from app.models import user_schema
from app.errors import error_response


@bp.route("/users", methods=["GET"])
def get_users():
    return jsonify(user_schema.dump(db.list_users(), many=True))


@bp.route("/users/<int:id>", methods=["GET"])
def get_user(id):
    user = db.find_user(id)
    if user is None:
        return error_response(404)
    return jsonify(user_schema.dump(user))
