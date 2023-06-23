from flask import Flask
from flask_cors import CORS
from flask_restful import Api

from auth import AuthRoutes
from config import Config

# 1.obj array          2.sqlite3              3.firestore  
# 4.obj array + jwt    5.google sheets api
from user5 import Users, User

app = Flask(__name__)

# 載入設定檔config.py所有設定
# 包括 flask-jwt-extended 的設定
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
    # 讀取config.py的配置
    app.config.from_object('config.Config')
    from flask import current_app
    # return {'DEBUG': current_app.config['DEBUG']}
    return {'DEBUG': current_app.config['JWT_SECRET_KEY']}

if __name__ == '__main__':
    app.run(debug=True)
