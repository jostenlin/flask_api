from flask_restful import Resource
from flask import request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # 設定 SQLite3 資料庫檔案路徑
db = SQLAlchemy(app)

# 定義資料庫模型
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)

# 創建資料庫表格（如果不存在）
db.create_all()

class Users(Resource):
    # 返回所有使用者
    def get(self):
        users = User.query.all()
        result = []
        for user in users:
            user_data = {
                'id': user.id,
                'name': user.name,
                'email': user.email
            }
            result.append(user_data)
        return result
    
class User(Resource):
    def get(self):
        # 取得使用者傳過來的 id
        id = request.args.get('id')
        user = User.query.filter_by(id=id).first()
        if user:
            result = {
                'id': user.id,
                'name': user.name,
                'email': user.email
            }
            return result
        return {'status': 'failure', 'message': 'User not found'}, 404

    def post(self):
        # 取得使用者傳過來的 JSON
        user_data = request.get_json()
        
        # 檢查使用者是否已經存在
        user = User.query.filter_by(id=user_data['id']).first()
        if user:
            return {'status': 'failure', 'message': 'User already exists'}, 400
            
        # 新增使用者
        new_user = User(id=user_data['id'], name=user_data['name'], email=user_data['email'])
        db.session.add(new_user)
        db.session.commit()
        result = {
            'status': 'success',
            'message': 'User added successfully',
            'added_user': {
                'id': new_user.id,
                'name': new_user.name,
                'email': new_user.email
            }
        }
        return result
    
    def delete(self):
        # 取得使用者傳過來的 id
        id = request.args.get('id')
        user = User.query.filter_by(id=id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            result = {
                'status': 'success',
                'message': 'User deleted',
                'deleted_user': {
                    'id': user.id,
                    'name': user.name,
                    'email': user.email
                }
            }
            return result
        return {'status': 'failure', 'message': 'User not found'}, 404
    
    def put(self):
        # 取得使用者傳過來的 JSON
        user_data = request.get_json()
        user = User.query.filter_by(id=user_data['id']).first()
        if user:
            user.name = user_data['name']
            user.email = user_data['email']
            db.session.commit()
            result = {
                'status': 'success',
                'message': 'User updated successfully',
                'updated_user': {
                    'id': user.id,
                    'name': user.name,
                    'email': user.email
                }
            }
            return result
        return {'status': 'failure', 'message': 'User not found'}, 404
