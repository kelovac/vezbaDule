from db import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    password = db.Column(db.String(80))
    user_created = db.Column(db.DateTime(),
                             nullable=False,
                             default=datetime.utcnow())
    user_updated = db.Column(db.DateTime(),
                             nullable=False,
                             default=datetime.utcnow())

    def __init__(self, username, first_name, last_name, password, user_created):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.user_created = user_created

    def json(self):
        return {'username': self.username,
                'first_name': self.first_name,
                'last_name': self.last_name,
                'password': self.password,
                'user_created': self.user_created.strftime('%Y-%m-%d %H:%M:%S')}

    def upd_json(self):
        return {'username': self.username,
                'first_name': self.first_name,
                'last_name': self.last_name,
                'password': self.password,
                'user_created': self.user_created.strftime('%Y-%m-%d %H:%M:%S'),
                'user_updated': self.user_updated.strftime('%Y-%m-%d %H:%M:%S')}

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
