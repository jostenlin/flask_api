from flask_restful import Resource
from flask import request
import pymysql
from collections import namedtuple


class Users(Resource):
    # 建構式
    def __init__(self):
        # 建立與 Google Cloud SQL MySQL 資料庫的連線
        self.conn = pymysql.connect(
            user="root",
            password="1234",
            db="users",
            # google cloud sql mysql
            host="35.229.211.35",
            # 本機mysql
            # host="localhost",
            # 將資料轉換為字典格式
            cursorclass=pymysql.cursors.DictCursor
            # 指向 App Engine 中與 Cloud SQL instance 的連接端點
            # unix_socket="/cloudsql/project_id:region:cloud_sql_instance_name",
            unix_socket="/cloudsql/my-project-0711-392510:asia-east1:mysqldb"
        )
        self.cursor = self.conn.cursor()

        # 建立 users 資料表（如果不存在）
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INT PRIMARY KEY,
                name VARCHAR(255),
                email VARCHAR(255)
            )
        """
        )
        self.conn.commit()

    def get(self):
        # 從資料庫中取得所有使用者
        self.cursor.execute("SELECT * FROM users")
        users = self.cursor.fetchall()
        return users


class User(Resource):
    # 建構式
    def __init__(self):
        # 建立與 Google Cloud SQL MySQL 資料庫的連線
        self.conn = pymysql.connect(
            user="root",
            password="1234",
            db="users",
            # google cloud sql mysql
            host="35.229.211.35",
            # 本機mysql
            # host="localhost",
            # 將資料轉換為字典格式
            cursorclass=pymysql.cursors.DictCursor
            # 指向 App Engine 中與 Cloud SQL instance 的連接端點
            # unix_socket="/cloudsql/project_id:region:cloud_sql_instance_name",
            unix_socket="/cloudsql/my-project-0711-392510:asia-east1:mysqldb"
        )
       
        
        self.cursor = self.conn.cursor()

    def get(self):
        # 取得使用者傳過來的 id
        id = request.args.get("id")

        # 從資料庫中查詢符合 id 的使用者
        self.cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
        user = self.cursor.fetchone()

        if user:
            return user
        else:
            return {"status": "failure", "message": "User not found"}, 404

    def post(self):
        # 取得使用者傳過來的 json
        user = request.get_json()

        # 檢查使用者是否已經存在
        self.cursor.execute("SELECT * FROM users WHERE id = %s", (user["id"],))
        existing_user = self.cursor.fetchone()
        if existing_user:
            return {"status": "failure", "message": "User already exists"}, 400

        # 新增使用者到資料庫
        self.cursor.execute(
            "INSERT INTO users (id, name, email) VALUES (%s, %s, %s)",
            (user["id"], user["name"], user["email"]),
        )
        self.conn.commit()

        result = {
            "status": "success",
            "message": "User added successfully",
            "added_user": user,
        }
        return result

    def delete(self):
        # 取得使用者傳過來的 id
        id = request.args.get("id")

        # 從資料庫中刪除符合 id 的使用者
        self.cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
        user = self.cursor.fetchone()

        if user:
            self.cursor.execute("DELETE FROM users WHERE id = %s", (id,))
            self.conn.commit()

            result = {
                "status": "success",
                "message": "User deleted",
                "deleted_user": user,
            }
            return result
        else:
            return {"status": "failure", "message": "User not found"}, 404

    def put(self):
        # 取得使用者傳過來的 json
        user = request.get_json()

        # 檢查使用者是否存在
        self.cursor.execute("SELECT * FROM users WHERE id = %s", (user["id"],))
        existing_user = self.cursor.fetchone()
        if not existing_user:
            return {"status": "failure", "message": "User not found"}, 404

        # 更新使用者資訊
        self.cursor.execute(
            "UPDATE users SET name = %s, email = %s WHERE id = %s",
            (user["name"], user["email"], user["id"]),
        )
        self.conn.commit()

        result = {
            "status": "success",
            "message": "User updated successfully",
            "updated_user": user,
        }
        return result
