from flask_restful import Resource
from flask import request
import jwt

users = [
            {
                'id': 1,
                'name': 'John Doe',
                'email': '1@abc.com'
            },
            {
                'id': 2,
                'name': 'Jane Doe',
                'email': '2@abc.com'
            }
        ]


class Users(Resource):
    # 返回所有使用者
    def get(self):
        return users
    

class User(Resource):        
    def get(self):
        # 取得使用者傳過來的id
        id = request.args.get('id')
        for user in users:
            if user['id'] == int(id):
                return user
        return {'status': 'failure', 'message': 'User not found'},404

    def post(self):
        # 取得使用者傳過來的json
        user=request.get_json()
        
        # 檢查使用者是否已經存在
        for u in users:
            if u['id'] == user['id']:
                return {'status': 'failure', 'message': 'User already exists'},400
            
        # 新增使用者
        users.append(user)
        result= {
                    'status': 'success', 
                    'message': 'User added successfully',
                    'added_user': user 
                }
        return result
    
    def delete(self):
        # 取得使用者傳過來的id
        id = request.args.get('id')
        for user in users:
            if user['id'] == int(id):
                users.remove(user)
                result= {
                    'status': 'success', 
                    'message': 'User deleted',
                    'deleted_user': user 
                }
                return result
        return {'status': 'failure', 'message': 'User not found'},404
    
    def put(self):
        # 取得使用者傳過來的json
        user=request.get_json()
        for i in range(len(users)):
            if users[i]['id'] == user['id']:
                users[i]=user
                result= {
                    'status': 'success', 
                    'message': 'User updated successfully',
                    'updated_user': user 
                }
                return result
        return {'status': 'failure', 'message': 'User not found'},404