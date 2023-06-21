from flask import request
from flask_jwt_extended import create_access_token, JWTManager

class AuthRoutes:
    @staticmethod
    def configure_routes(app):        
        # 建立 Flask-JWT-Extended 實例
        JWTManager(app)

        # 登入以取得 JWT Token
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
