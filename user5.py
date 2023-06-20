from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
import jwt
from flask_jwt_extended import create_access_token

users = [
    {
        'id': 1,
        'name': 'John Doe',
        'email': '1@abc.com'
    },
    {
        'id': 2,
        'name': 'Jane Doe',
        'email': '2@abc.com'
    }
]


class Users(Resource):
    # 返回所有使用者
    @jwt_required  # 需要 JWT 認證
    def get(self):
        return users


class User(Resource):
    @jwt_required  # 需要 JWT 認證
    def get(self):
        # 取得使用者傳過來的id
        id = request.args.get('id')
        for user in users:
            if user['id'] == int(id):
                return user
        return {'status': 'failure', 'message': 'User not found'}, 404

    def post(self):
        # 取得使用者傳過來的json
        user = request.get_json()

        # 檢查使用者是否已經存在
        for u in users:
            if u['id'] == user['id']:
                return {'status': 'failure', 'message': 'User already exists'}, 400

        # 新增使用者
        users.append(user)
        result = {
            'status': 'success',
            'message': 'User added successfully',
            'added_user': user
        }
        return result

    def delete(self):
        # 取得使用者傳過來的id
        id = request.args.get('id')
        for user in users:
            if user['id'] == int(id):
                users.remove(user)
                result = {
                    'status': 'success',
                    'message': 'User deleted',
                    'deleted_user': user
                }
                return result
        return {'status': 'failure', 'message': 'User not found'}, 404

    def put(self):
        # 取得使用者傳過來的json
        user = request.get_json()
        for i in range(len(users)):
            if users[i]['id'] == user['id']:
                users[i] = user
                result = {
                    'status': 'success',
                    'message': 'User updated successfully',
                    'updated_user': user
                }
                return result
        return {'status': 'failure', 'message': 'User not found'}, 404


# 建立 JWT 金鑰
app.config['JWT_SECRET_KEY'] = 'super-secret'  # 修改為你自己的金鑰

# 建立 Flask-JWT-Extended 實例
jwt = JWTManager(app)


# 產生 JWT Token
@app.route('/login', methods=['POST'])
def login():
    # 取得使用者傳過來的 JSON
    credentials = request.get_json()
    
    # 檢查使用者的帳號密碼是否正確
    username = credentials.get('username')
    password = credentials.get('password')
    if username == 'admin' and password == 'password':
        access_token = create_access_token(identity=username)
        return {'access_token': access_token}, 200
    else:
        return {'error': 'Invalid username or password'}, 401
