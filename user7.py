from flask_restful import Resource
from flask import request
import sqlite3


class Users(Resource):
    def get(self):
        with sqlite3.connect("/mnt/my_db_files/users.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()
            return users


class User(Resource):
    def get(self):
        with sqlite3.connect("/mnt/my_db_files/users.db") as conn:
            cursor = conn.cursor()

            # 取得使用者傳過來的 id
            id = request.args.get("id")

            # 從資料庫中查詢符合 id 的使用者
            cursor.execute("SELECT * FROM users WHERE id = ?", (id,))
            user = cursor.fetchone()

            if user:
                return {"id": user[0], "name": user[1], "email": user[2]}
            else:
                return {"status": "failure", "message": "User not found"}, 404

    def post(self):
        with sqlite3.connect("/mnt/my_db_files/users.db") as conn:
            cursor = conn.cursor()

            # 取得使用者傳過來的 json
            user = request.get_json()

            # 檢查使用者是否已經存在
            cursor.execute("SELECT * FROM users WHERE id = ?", (user["id"],))
            existing_user = cursor.fetchone()
            if existing_user:
                return {"status": "failure", "message": "User already exists"}, 400

            # 新增使用者到資料庫
            cursor.execute(
                "INSERT INTO users (id, name, email) VALUES (?, ?, ?)",
                (user["id"], user["name"], user["email"]),
            )
            conn.commit()

            result = {
                "status": "success",
                "message": "User added successfully",
                "added_user": user,
            }
            return result

    def delete(self):
        with sqlite3.connect("/mnt/my_db_files/users.db") as conn:
            cursor = conn.cursor()
            # 取得使用者傳過來的 id
            id = request.args.get("id")

            # 從資料庫中刪除符合 id 的使用者
            cursor.execute("SELECT * FROM users WHERE id = ?", (id,))
            user = cursor.fetchone()

            if user:
                cursor.execute("DELETE FROM users WHERE id = ?", (id,))
                conn.commit()

                result = {
                    "status": "success",
                    "message": "User deleted",
                    "deleted_user": {"id": user[0], "name": user[1], "email": user[2]},
                }
                return result
            else:
                return {"status": "failure", "message": "User not found"}, 404

    def put(self):
        with sqlite3.connect("/mnt/my_db_files/users.db") as conn:
            cursor = conn.cursor()
            # 取得使用者傳過來的 json
            user = request.get_json()

            # 檢查使用者是否存在
            cursor.execute("SELECT * FROM users WHERE id = ?", (user["id"],))
            existing_user = cursor.fetchone()
            if not existing_user:
                return {"status": "failure", "message": "User not found"}, 404

            # 更新使用者資訊
            cursor.execute(
                "UPDATE users SET name = ?, email = ? WHERE id = ?",
                (user["name"], user["email"], user["id"]),
            )
            conn.commit()

            result = {
                "status": "success",
                "message": "User updated successfully",
                "updated_user": user,
            }
            return result
