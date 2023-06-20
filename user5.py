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

'''
我們使用 flask_jwt_extended 模組的 JWTManager 來管理 JWT 認證。
首先，我們設定了 JWT 的金鑰 JWT_SECRET_KEY，你需要將其修改為一個安全且隨機的字串。
接下來，我們在 Users 和 User 類別的方法上使用了 @jwt_required 裝飾器，
這表示這些方法需要 JWT 認證才能訪問。最後，我們新增了一個 /login 的路由，
用於驗證使用者的帳號密碼並產生 JWT Token。

請確保你已經安裝了 Flask-JWT-Extended 套件，可以使用以下命令進行安裝：
pip install flask-jwt-extended
請注意，這只是一個示例程式碼，實際的 JWT 實作可能需要更多的安全措施，
例如使用 HTTPS 進行傳輸、適當的 Token 過期時間等。
請仔細閱讀 Flask-JWT-Extended 的文件以瞭解更多詳細信息。

'''