from flask_restful import Resource
from flask import request

# Google Sheets API v4 版本
import gspread
from google.oauth2.service_account import Credentials

def getUsers():
    # 設定 Google Sheets API 的驗證憑證
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    credentials = Credentials.from_service_account_file('sheet_api_key.json', scopes=scope)
    client = gspread.authorize(credentials)
    
    # 開啟 Google Sheets
    # 注意：google sheet必須與服務帳號共用編輯
    # 一個服務帳號可以共用多個google sheet
    # 返回哪一個共用的sheet以sheet名稱(如'test')為準
    sheet = client.open('test').worksheet('工作表1')  

    # 讀取資料
    data = sheet.get_all_records()

    # 篩選
    # data = [record for record in data if record['name'] == 'kevin']

    # 處理資料並回傳
    return data

users = getUsers()

# 增刪改都是假的，資料都在記憶體中
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