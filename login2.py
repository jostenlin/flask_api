from flask_restful import Resource
from flask import request

admin={
  "success": True,
  "data": {
    "username": "admin",
    "roles": ["admin"],
    "accessToken": "eyJhbGciOiJIUzUxMiJ9.admin",
    "refreshToken": "eyJhbGciOiJIUzUxMiJ9.adminRefresh",
    "expires": "2023/10/30 00:00:00"
  }
}

common={
  "success": True,
  "data": {
    "username": "common",
    "roles": ["common"],
    "accessToken": "eyJhbGciOiJIUzUxMiJ9.common",
    "refreshToken": "eyJhbGciOiJIUzUxMiJ9.commonRefresh",
    "expires": "2023/10/30 00:00:00"
  }
}

class Login2(Resource):
    def post(self):
        username = request.get_json()['username']
        if username == 'admin':
            return admin
        return common