# coding=utf-8
from datetime import datetime
import uuid
from hashlib import sha224

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy import or_


BASE = declarative_base()

class IDMixin(object):
    """ID mixin"""
    id = Column(Integer, primary_key=True)


class UUIDMixin(object):
    """UUID mixin"""
    id = Column(String(32), default=lambda: uuid.uuid4().hex, primary_key=True)


class TimestampMixin(object):
    """Timestamp mixin"""
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class User(BASE, UUIDMixin, TimestampMixin):
    __tablename__ = 'users'
    
    username = Column(String(64), unique=True, index=True)
    nickname = Column(String(64), nullable=True)
    email = Column(String(128), unique=True, index=True)
    password_hash = Column(String(128), nullable=False)
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        self.password_hash = sha224(password.encode('utf-8')).hexdigest()
    
    def verify_password(self, password):
        return self.password_hash == sha224(password.encode('utf-8')).hexdigest()
    
    @staticmethod
    def get_user(session, username_or_email):
        return session.query(User).filter(or_(User.username == username_or_email, 
            User.email == username_or_email)).first()