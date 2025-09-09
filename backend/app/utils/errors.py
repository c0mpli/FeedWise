from flask import jsonify

class APIError(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        rv['error'] = True
        return rv

class ValidationError(APIError):
    status_code = 400

class NotFoundError(APIError):
    status_code = 404

class ConflictError(APIError):
    status_code = 409

class InternalServerError(APIError):
    status_code = 500

def handle_api_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response