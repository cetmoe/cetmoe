from flask_sqlalchemy import SQLAlchemy
from .app import db

class User(db.Model):
    __tablename__ = 'table_name'

    bnet = db.Column(db.VARCHAR, primary_key = True)
    avatar = db.Column(db.VARCHAR)
    authenticated = db.Column(db.Boolean, default=False)


    def __init__(self, bnet):
        self.bnet = bnet

    def is_active(self):
        return true

    def get_id(self):
        return self.bnet

    def is_autenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return False

    def __repr__(self):
        return '<User %r>' % self.bnet

