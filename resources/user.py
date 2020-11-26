from flask_restful import Resource, reqparse
from models.user import UserModel
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('first_name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                    )
    parser.add_argument('last_name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                    )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                    )

    def get(self, username):
        user = UserModel.find_by_username(username)
        if user:
            return user.json()
        return {'message': 'User not found'}, 404

    def post(self, username):
        if UserModel.find_by_username(username):
            return {'message': "User with username '{}' already exists.".format(username)}

        data = User.parser.parse_args()

        hashed_password = generate_password_hash(data['password'], method='sha256')

        user = UserModel(username=username,
                 first_name=data['first_name'],
                 last_name=data['last_name'],
                 password=hashed_password,
                 user_created=datetime.utcnow())

        try:
            user.save_to_db()
        except:
            return {'message': "An error occured inserting the user."}, 500

        return user.json(), 201

    def delete(self, username):
        user = UserModel.find_by_username(username)
        if user:
            user.delete_from_db()

        return {'message': 'User deleted.'}

    def put(self, username):
        data = User.parser.parse_args()

        user = UserModel.find_by_username(username)

        if user is None:
            user = UserModel(username=username,
                     first_name=data['first_name'],
                     last_name=data['last_name'],
                     password=data['password'],
                     user_updated=datetime.utcnow())
        else:
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.password = data['password']
            user.user_updated = datetime.utcnow()

        user.save_to_db()

        return user.upd_json()


class UserList(Resource):
    def get(self):
        return {'users': [user.json() for user in UserModel.query.all()]}
