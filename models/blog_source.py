# coding=utf-8
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from sqlalchemy.exc import IntegrityError

from . import BASE, UUIDMixin, TimestampMixin


class BlogSource(BASE, UUIDMixin, TimestampMixin):
    """original sources of blogs"""
    __tablename__ = 'blog_sources'
    
    name = Column(String(50), unique=True, nullable=True)
    
    blogs = relationship('Blog', backref='source', 
        cascade='all, delete-orphan', lazy='dynamic')

    @staticmethod
    def insert_default_sources(db_session):
        names = ['原创', '转载', '翻译']
        for name in names:
            source = BlogSource(name=name)
            db_session.add(source)
        try:
            db_session.commit()
        except IntegrityError:
            db_session.rollback()
            print('Default blog sources already exist!')
        else:
            print('Insert default blog sources: %s' % names)