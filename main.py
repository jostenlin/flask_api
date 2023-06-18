from flask import Flask
from flask import request
from flask import jsonify

app = Flask(__name__)

# 使用config.py的設定
app.config.from_object('config.Config')

# 匯入目前的app
from flask import current_app

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

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/users', methods=['GET'])
def getUsers():
    # 如果methods有幾種方法，也可以根據不同的方法做不同的事情
    # if request.method != 'GET':
    #     pass
    return jsonify(users)

@app.route('/adduser', methods=['POST'])
def addUser():
    user=request.get_json()
    users.append(user)
    result= {
                'status': 'success', 
                'message': 'User added successfully',
                'added_user': user 
            }
    return jsonify(result)

# given an id, delete the user
@app.route('/deleteuser/<int:id>', methods=['DELETE'])
def deleteUser(id):
    for user in users:
        if user['id'] == id:
            users.remove(user)
            result= {
                'status': 'success', 
                'message': 'User deleted successfully',
                'removed_user': user 
            }
            return jsonify(result)
    return jsonify({'status': 'failure', 'message': 'User not found'})

# given an user, update the user
# user is passed as json in the request body
@app.route('/updateuser', methods=['PUT'])
def updateUser():
    user=request.get_json()
    for i in range(len(users)):
        if users[i]['id'] == user['id']:
            users[i]=user
            result= {
                'status': 'success', 
                'message': 'User updated successfully',
                'updated_user': user 
            }
            return jsonify(result)
    return jsonify({'status': 'failure', 'message': 'User not found'})

if __name__ == '__main__':
    app.run(debug=True)
