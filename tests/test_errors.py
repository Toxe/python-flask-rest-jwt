from app.errors import error_response


def test_error_response_has_all_basic_fields(app):
    response = error_response(404)
    assert response.status_code == 404
    assert response.is_json == True
    json = response.get_json()
    assert json != None
    assert "error" in json


def test_error_with_message(app):
    response = error_response(404, "Resource not found.")
    json = response.get_json()
    assert "message" in json
    assert json["message"] == "Resource not found."


def test_error_without_message(app):
    response = error_response(404)
    assert "message" not in response.get_json()


def test_generic_400_error(app):
    response = error_response(400)
    assert response.status_code == 400
    assert response.get_json()["error"] == "Bad Request"


def test_generic_404_error(app):
    response = error_response(404)
    assert response.status_code == 404
    assert response.get_json()["error"] == "Not Found"


def test_generic_500_error(app):
    response = error_response(500)
    assert response.status_code == 500
    assert response.get_json()["error"] == "Internal Server Error"
