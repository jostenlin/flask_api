from flask import Flask
from flask import request

app = Flask(__name__)

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
    return users

@app.route('/adduser', methods=['POST'])
def addUser():
    user=request.get_json()
    users.append(user)    
    return {
                'status': 'success', 
                'message': 'User added successfully',
                'added_user': user 
           }

if __name__ == '__main__':
    app.run(debug=True)
