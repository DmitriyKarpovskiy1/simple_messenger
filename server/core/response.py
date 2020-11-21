from flask import jsonify


def response(status_code, message, sensible=None):
    payload = {}
    payload["content"] = message
    payload["sensible"] = sensible
    response = jsonify(payload)
    response.status_code = status_code
    return response
