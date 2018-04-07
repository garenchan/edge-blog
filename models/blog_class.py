# coding=utf-8
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func

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
        return_total = kwargs.pop('return_total', False)
        
        query = db_session.query(BlogClass)
        total = query.count()
        if search is not None:
            query = query.filter(BlogClass.name.contains(search))
        # NOTE: We always show blog_classes in ascending order of `order`
        query = query.order_by(BlogClass.order.asc())
        if offset is not None:
            query = query.offset(offset)
        if limit is not None:
            query = query.limit(limit)
            
        if return_total:
            # return items' total and display items
            return total, query.all()
        else:
            return query.all()

    @staticmethod
    def delete_blog_class(db_session, class_id):
        """Delete blog class of specified ID"""
        blog_class = db_session.query(BlogClass).filter(
                BlogClass.id == class_id).first()
        if blog_class:
            db_session.delete(blog_class)
            db_session.commit()
        return blog_class

    @staticmethod
    def get_max_order(db_session):
        max_order = db_session.query(func.max(BlogClass.order)).scalar()
        if max_order is None:
            max_order = BlogClass.order.default.arg - 1
        return max_order

    @staticmethod
    def insert_blog_class(db_session, **kwargs):
        name = kwargs.pop('name')
        description = kwargs.pop('description', '')
        blog_class = BlogClass(name=name, description=description)
        blog_class.order = BlogClass.get_max_order(db_session) + 1
        db_session.add(blog_class)
        db_session.commit()
        return blog_class