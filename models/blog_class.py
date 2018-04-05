# coding=utf-8
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.exc import IntegrityError

from . import BASE, UUIDMixin, TimestampMixin


class BlogClass(BASE, UUIDMixin, TimestampMixin):
    """blog's class: used for classify"""
    __tablename__ = 'blog_classes'
    
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(100), nullable=True)
    # The smaller `order` value is, the more it is ahead
    order = Column(Integer, default=1, nullable=False)
    
    subclasses = relationship('BlogSubClass', backref='cls', 
        cascade='all, delete-orphan', lazy='dynamic')

    @staticmethod
    def insert_default_classes(db_session):
        class_infos = [
            dict(name='数据库', description='数据库知识', order=1),
            dict(name='前端', description='前端知识', order=2),
            dict(name='后端', description='后端知识', order=3),
        ]
        for info in class_infos:
            _class = BlogClass(**info)
            db_session.add(_class)
        try:
            db_session.commit()
        except IntegrityError:
            db_session.rollback()
            print('Default blog classes already exist!')
        else:
            print('Insert default blog classes: %s' % class_infos)

    @staticmethod
    def get_blog_classes(db_session, **kwargs):
        search = kwargs.pop('search', None)
        offset = kwargs.pop('offset', None)
        limit = kwargs.pop('limit', None)
        
        query = db_session.query(BlogClass)
        if search is not None:
            query = query.filter(BlogClass.name.contains(search))
        # NOTE: We always show blog_classes in ascending order of `order`
        query = query.order_by(BlogClass.order.asc())
        if offset is not None:
            query = query.offset(offset)
        if limit is not None:
            query = query.limit(limit)
            
        return query.all()