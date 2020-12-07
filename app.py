import os
from flask import Flask, request, jsonify, flash, session
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from db import db
from resources.user import User, UserList
from models.user import UserModel
from werkzeug.security import generate_password_hash, check_password_hash, safe_str_cmp

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
api = Api(app)
db.init_app(app)

@app.before_first_request
def create_table():
    db.create_all()


api.add_resource(User, '/user/<string:username>')
api.add_resource(UserList, '/users')

@app.route('/login', methods=['POST', 'GET', 'PUT', 'DELETE'])
def login():
    if request.method == "POST":

        data = request.get_json()

        username = data['username']
        password = data['password']

        user = UserModel.find_by_username(username=username)

        if user and check_password_hash(user.password, password):
            return jsonify({"response": "user is valid"}), 200
        else:
            return jsonify({"response": "Invalid username or password."}), 400
    return jsonify({"error": "Please use post method"}), 405
#"""
#prima username i password
#proverava u bazi da li su validni
#i vraca True ili False
#"""

if __name__ == '__main__':
    app.run(port=5000, debug=True)
