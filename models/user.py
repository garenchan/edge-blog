# coding=utf-8
from hashlib import sha224

from sqlalchemy import Column, String
from sqlalchemy import or_

from . import BASE, UUIDMixin, TimestampMixin
from contrib.session import UserMixin


class User(BASE, UUIDMixin, TimestampMixin, UserMixin):
    __tablename__ = 'users'
    
    username = Column(String(64), unique=True, index=True)
    nickname = Column(String(64), nullable=True)
    email = Column(String(128), unique=True, index=True)
    password_hash = Column(String(128), nullable=False)

    @property
    def password(self):
        # raise AttributeError('password is not a readable attribute')
        return self.password_hash

    @password.setter
    def password(self, password):
        self.password_hash = sha224(password.encode('utf-8')).hexdigest()

    def verify_password(self, password):
        return self.password_hash == sha224(password. \
            encode('utf-8')).hexdigest()

    @staticmethod
    def get_user_by_username_email(db_session, username_or_email):
        return db_session.query(User).filter(or_(User.username == \
            username_or_email, User.email == username_or_email)).first()

    @staticmethod
    def get_user_by_id(db_session, user_id):
        return db_session.query(User).filter(User.id == user_id).first()