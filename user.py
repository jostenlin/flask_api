from flask_restful import Resource
from flask import request
import firebase_admin
from firebase_admin import credentials, firestore

# 初始化 Firebase
cred = credentials.Certificate('key.json')
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
        id = request.args.get('id')
        # 取得特定使用者的文件
        user_doc = db.collection("users").document(id).get()
        if user_doc.exists:
            return user_doc.to_dict()
        else:
            return {'status': 'failure', 'message': 'User not found'}, 404

    def post(self):
        user = request.get_json()
        id = user['id']
        # 檢查使用者是否已經存在
        user_doc = db.collection("users").document(id).get()
        if user_doc.exists:
            return {'status': 'failure', 'message': 'User already exists'}, 400
        # 新增使用者到資料庫
        db.collection("users").document(id).set(user)
        result = {
            'status': 'success',
            'message': 'User added successfully',
            'added_user': user
        }
        return result

    def delete(self):
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
        id = user['id']
        # 檢查使用者是否存在
        user_doc = db.collection("users").document(id).get()
        if not user_doc.exists:
            return {'status': 'failure', 'message': 'User not found'}, 404
        # 更新使用者資訊
        db.collection("users").document(id).set(user)
        result = {
            'status': 'success',
            'message': 'User updated successfully',
            'updated_user': user
        }
        return result
