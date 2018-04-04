# coding=utf-8
from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from . import BASE, UUIDMixin, TimestampMixin


class BlogSubClass(BASE, UUIDMixin, TimestampMixin):
    """blog's class: used for classify"""
    __tablename__ = 'blog_subclasses'
    
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(100), nullable=True)
    protected = Column(Boolean, default=False)
    
    class_id = Column(String(32), ForeignKey('blog_classes.id'), nullable=False)
    blogs = relationship('Blog', backref='subclass', 
        cascade='all, delete-orphan', lazy='dynamic')

