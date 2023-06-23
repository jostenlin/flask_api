from flask_restful import Resource
from flask import request
import firebase_admin
from firebase_admin import credentials, firestore

# 初始化 Firebase
cred = credentials.Certificate('firebase.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

class Users(Resource):
    def get(self):
        # 取得 users 集合的所有文件
        users_ref = db.collection("users")
        users = [doc.to_dict() for doc in users_ref.stream()]
        return users

class User(Resource):
    def get(self):
        # 從網址取得 id 參數(string)
        id = request.args.get('id')
        
        # 從firestore取得索引為id的使用者資料
        user_doc = db.collection("users").document(id).get()
        if user_doc.exists:
            return user_doc.to_dict()
        else:
            return {'status': 'failure', 'message': 'User not found'}, 404

    def post(self):
        # 從請求中的body取得使用者資料
        user = request.get_json()
        
        # 從使用者資料中取得id(string)
        id = str(user['id'])
        
        # 檢查索引為id的使用者是否已經存在
        user_doc = db.collection("users").document(id).get()
        if user_doc.exists:
            return {'status': 'failure', 'message': '該id使用者已存在'}, 400
            
        # 新增使用者到資料庫(注意自訂id為字串)
        db.collection("users").document(id).set(user)
        result = {
            'status': 'success',
            'message': 'User added successfully',
            'added_user': user
        }
        return result

    def delete(self):
        # 從網址取得 id querystring
        id = request.args.get('id')
        
        # 檢查使用者是否存在
        user_doc = db.collection("users").document(id).get()
        if user_doc.exists:
            # 刪除使用者
            db.collection("users").document(id).delete()
            result = {
                'status': 'success',
                'message': 'User deleted',
                'deleted_user': user_doc.to_dict()
            }
            return result
        else:
            return {'status': 'failure', 'message': 'User not found'}, 404

    def put(self):
        user = request.get_json()
        id = str(user['id'])
        
        # 檢查使用者是否存在
        user_doc = db.collection("users").document(id).get()
        if not user_doc.exists:
            return {'status': 'failure', 'message': '該使用者不存在'}, 404
        
        # 更新使用者資訊
        db.collection("users").document(id).set(user)
        result = {
            'status': 'success',
            'message': 'User updated successfully',
            'updated_user': user
        }
        return result
