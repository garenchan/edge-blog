# coding=utf-8
import uuid
from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, Integer, String

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

# NOTE: When add a new model, we need to import here, or else alembic cannot
#   aware of its existence
from .user import User
from .blog_source import BlogSource
from .blog_class import BlogClass
from .blog_subclass import BlogSubClass
from .blog import Blog