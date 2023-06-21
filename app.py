from flask import Flask
from flask_cors import CORS
from flask_restful import Api

from auth import AuthRoutes
from user import Users, User
from config import Config

app = Flask(__name__)

# 載入設定檔
app.config.from_object(Config)

# 允許跨域請求
CORS(app)

# 設定權限相關路由
AuthRoutes.configure_routes(app)

# 設定其他路由
api = Api(app)
api.add_resource(Users, '/users')
api.add_resource(User, '/user')

# 測試用路由(可刪除)
@app.route('/')
def hello_world():
    # 使用config.py的設定
    app.config.from_object('config.Config')
    from flask import current_app
    # return {'DEBUG': current_app.config['DEBUG']}
    return {'DEBUG': current_app.config['JWT_SECRET_KEY']}

if __name__ == '__main__':
    app.run(debug=True)
