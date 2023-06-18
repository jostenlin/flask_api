from flask_restful import Resource
from flask import request
import sqlite3

class Users(Resource):
   
    # 建構式
    def __init__(self):

        # 建立 SQLite 資料庫連線
        self.conn = sqlite3.connect('users.db')
        self.cursor = self.conn.cursor()
    
        # 建立 users 資料表（如果不存在）
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT,
                email TEXT
            )
        ''')
        self.conn.commit()
    def get(self):
        # 從資料庫中取得所有使用者
        self.cursor.execute('SELECT * FROM users')
        users = self.cursor.fetchall()
        return users

class User(Resource):
    # 建構式
    def __init__(self):
        # 建立 SQLite 資料庫連線
        self.conn = sqlite3.connect('users.db')
        self.cursor = self.conn.cursor()

        # 建立 users 資料表（如果不存在）
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT,
                email TEXT
            )
        ''')
        self.conn.commit()
        
    def get(self):
        # 取得使用者傳過來的 id
        id = request.args.get('id')
        
        # 從資料庫中查詢符合 id 的使用者
        self.cursor.execute('SELECT * FROM users WHERE id = ?', (id,))
        user = self.cursor.fetchone()
        
        if user:
            return {
                'id': user[0],
                'name': user[1],
                'email': user[2]
            }
        else:
            return {'status': 'failure', 'message': 'User not found'}, 404

    def post(self):
        # 取得使用者傳過來的 json
        user = request.get_json()
        
        # 檢查使用者是否已經存在
        self.cursor.execute('SELECT * FROM users WHERE id = ?', (user['id'],))
        existing_user = self.cursor.fetchone()
        if existing_user:
            return {'status': 'failure', 'message': 'User already exists'}, 400
        
        # 新增使用者到資料庫
        self.cursor.execute('INSERT INTO users (id, name, email) VALUES (?, ?, ?)', (user['id'], user['name'], user['email']))
        self.conn.commit()
        
        result = {
            'status': 'success',
            'message': 'User added successfully',
            'added_user': user
        }
        return result

    def delete(self):
        # 取得使用者傳過來的 id
        id = request.args.get('id')
        
        # 從資料庫中刪除符合 id 的使用者
        self.cursor.execute('SELECT * FROM users WHERE id = ?', (id,))
        user = self.cursor.fetchone()
        
        if user:
            self.cursor.execute('DELETE FROM users WHERE id = ?', (id,))
            self.conn.commit()
            
            result = {
                'status': 'success',
                'message': 'User deleted',
                'deleted_user': {
                    'id': user[0],
                    'name': user[1],
                    'email': user[2]
                }
            }
            return result
        else:
            return {'status': 'failure', 'message': 'User not found'}, 404

    def put(self):
        # 取得使用者傳過來的 json
        user = request.get_json()
        
        # 檢查使用者是否存在
        self.cursor.execute('SELECT * FROM users WHERE id = ?', (user['id'],))
        existing_user = self.cursor.fetchone()
        if not existing_user:
            return {'status': 'failure', 'message': 'User not found'}, 404
        
        # 更新使用者資訊
        self.cursor.execute('UPDATE users SET name = ?, email = ? WHERE id = ?', (user['name'], user['email'], user['id']))
        self.conn.commit()
        
        result = {
            'status': 'success',
            'message': 'User updated successfully',
            'updated_user': user
        }
        return result
