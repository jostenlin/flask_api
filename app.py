from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from user import Users, User

app = Flask(__name__)

# 使用config.py的設定
app.config.from_object('config.Config')

# 匯入目前的app
from flask import current_app

# 允許跨域請求
CORS(app)

api = Api(app)

api.add_resource(Users, '/users')
api.add_resource(User, '/user')

# 測試用路由
@app.route('/')
def hello_world():
    return {'DEBUG': current_app.config['DEBUG']}

if __name__ == '__main__':
    app.run(debug=True)
