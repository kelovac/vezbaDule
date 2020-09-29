import os
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt import JWT

from db import db
from resources.user import User, UserList
from security import authenticate, identity

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWT(app, authenticate, identity)

api.add_resource(User, '/user/<string:username>')
api.add_resource(UserList, '/users')

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)
