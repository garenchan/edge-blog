# coding=utf-8
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship, backref, joinedload
from sqlalchemy.exc import IntegrityError

from . import BASE, UUIDMixin, TimestampMixin


class BlogSource(BASE, UUIDMixin, TimestampMixin):
    """original sources of blogs"""
    __tablename__ = 'blog_sources'
    
    name = Column(String(50), unique=True, nullable=True)
    # support lazy, joined, dynamic relationship loading
    blogs = relationship('Blog', backref=backref('source', lazy='joined'), 
        cascade='all, delete-orphan')
    blog_query = relationship('Blog', lazy='dynamic')

    @staticmethod
    def get_blog_sources(db_session, **kwargs):
        search = kwargs.pop('search', None)
        offset = kwargs.pop('offset', None)
        limit = kwargs.pop('limit', None)
        return_total = kwargs.pop('return_total', False)
        lazy = kwargs.pop('lazy', True)
        
        query = db_session.query(BlogSource)
        total = query.count()
        if search is not None:
            query = query.filter(BlogSource.name.contains(search))
        query = query.order_by(BlogSource.updated_at.desc())
        if offset is not None:
            query = query.offset(offset)
        if limit is not None:
            query = query.limit(limit)
        if not lazy:
            query = query.options(joinedload(BlogSource.blogs))
            
        if return_total:
            # return items' total and display items
            return total, query.all()
        else:
            return query.all()

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