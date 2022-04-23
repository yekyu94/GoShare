from flask import request
from flask_restx import Resource, Api, Namespace

Auth = Namespace(
    name="Auth",
    description="Auth & Make Key",
)

@Auth.route('')
class AuthPost(Resource):
    def post(self):
        print(request.json.get('data'))
        return {
            'data' : "test"
        }
