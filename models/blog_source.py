# coding=utf-8
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from . import BASE, UUIDMixin, TimestampMixin


class BlogSource(BASE, UUIDMixin, TimestampMixin):
    """original sources of blogs"""
    __tablename__ = 'blog_sources'
    
    name = Column(String(50), unique=True, nullable=True)
    
    blogs = relationship('Blog', backref='source', 
        cascade='all, delete-orphan', lazy='dynamic')