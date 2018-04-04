# coding=utf-8
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from . import BASE, UUIDMixin, TimestampMixin


class BlogClass(BASE, UUIDMixin, TimestampMixin):
    """blog's class: used for classify"""
    __tablename__ = 'blog_classes'
    
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(100), nullable=True)
    order = Column(Integer, default=1, nullable=False)
    
    subclasses = relationship('BlogSubClass', backref='class', 
        cascade='all, delete-orphan', lazy='dynamic')