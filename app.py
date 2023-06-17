from flask import Flask
from flask_restful import Api
from user import Users, User

app = Flask(__name__)
api = Api(app)

api.add_resource(Users, '/users')
api.add_resource(User, '/user')

if __name__ == '__main__':
    app.run(debug=True)
