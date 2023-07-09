import os
from flask import Flask
from flask_restful import Api

from auth import AuthRoutes
from config import Config

# 1.obj array          2.sqlite3              3.firestore
# 4.obj array + jwt    5.google sheets api
from user2 import Users, User

from login2 import Login2
from asyncRoutes import AsyncRoutes

from google.cloud import storage


def download_file(bucket_name, object_name, local_path):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(object_name)
    blob.download_to_filename(local_path)


app = Flask(__name__)

# 允許跨域請求
# from flask_cors import CORS
# CORS(app)

# 載入設定檔config.py所有設定
# 包括 flask-jwt-extended 的設定
app.config.from_object(Config)

# 設定權限相關路由
AuthRoutes.configure_routes(app)

# 設定其他路由
api = Api(app)
api.add_resource(Users, "/users")
api.add_resource(User, "/user")
api.add_resource(Login2, "/login2")
api.add_resource(AsyncRoutes, "/getAsyncRoutes")


# 測試用路由(可刪除)
@app.route("/")
def hello_world():
    # 讀取config.py的配置
    app.config.from_object("config.Config")
    from flask import current_app

    # return {'DEBUG': current_app.config['DEBUG']}
    # return {"DEBUG": current_app.config["JWT_SECRET_KEY"]}
    return "hi:" + os.environ.get("DB_URL")


@app.route("/newdb")
def newdb():
    download_file("test-sqlite3", "users.db", "./users.db")
    return "從storage下載新的資料庫"


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=8888)
