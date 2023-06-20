from flask import Flask, request
from flask_cors import CORS
from flask_restful import Api
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_jwt_extended import  create_access_token, JWTManager
import jwt

from user import Users, User

app = Flask(__name__)

# 使用config.py的設定
app.config.from_object('config.Config')

# 匯入目前的app
from flask import current_app

# 允許跨域請求
CORS(app)

# 設定路由
api = Api(app)
api.add_resource(Users, '/users')
api.add_resource(User, '/user')

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


# 測試用路由
@app.route('/')
def hello_world():
    return {'DEBUG': current_app.config['DEBUG']}

if __name__ == '__main__':
    app.run(debug=True)
