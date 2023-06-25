from flask_restful import Resource
from flask import request
import json
import gspread
from google.oauth2.service_account import Credentials

# 設定 Google Sheets 的認證範圍和金鑰檔案路徑
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = Credentials.from_service_account_file('sheet_api_key.json', scopes=scope)
client = gspread.authorize(credentials)

# 開啟 Google Sheets
# 注意：google sheet必須與服務帳號共用編輯
# 一個服務帳號可以共用多個google sheet
# 返回哪一個共用的sheet以sheet名稱(如'test')為準
sheet = client.open('test').worksheet('工作表1') 

class Users(Resource):
    def get(self):
        # 讀取所有使用者資料
        data = sheet.get_all_records()
        return data

class User(Resource):
    def get(self):
        id = request.args.get('id')
        data = sheet.get_all_records()
        for user in data:
            if user['id'] == int(id):
                return user
        return {'status': 'failure', 'message': 'User not found'}, 404

    def post(self):
        user = request.get_json()
        data = sheet.get_all_records()
        for u in data:
            if u['id'] == user['id']:
                return {'status': 'failure', 'message': 'User already exists'}, 400
        sheet.append_row([user['id'], user['name'], user['email']])
        result = {
            'status': 'success',
            'message': 'User added successfully',
            'added_user': user
        }
        return result

    def delete(self):
        id = request.args.get('id')
        data = sheet.get_all_records()
        for i, user in enumerate(data):
            if user['id'] == int(id):
                row = i + 2  # 因為資料從第二列開始，所以需要加上偏移量
                sheet.delete_row(row)
                result = {
                    'status': 'success',
                    'message': 'User deleted',
                    'deleted_user': user
                }
                return result
        return {'status': 'failure', 'message': 'User not found'}, 404

    def put(self):
        user = request.get_json()
        data = sheet.get_all_records()
        for i, u in enumerate(data):
            if u['id'] == user['id']:
                row = i + 2  # 因為資料從第二列開始，所以需要加上偏移量
                cell_range = f"A{row}:C{row}"
                values = [user['id'], user['name'], user['email']]
                sheet.update(cell_range, [values])
                result = {
                    'status': 'success',
                    'message': 'User updated successfully',
                    'updated_user': user
                }
                return result
        return {'status': 'failure', 'message': 'User not found'}, 404