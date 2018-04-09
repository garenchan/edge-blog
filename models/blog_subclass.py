# coding=utf-8
from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref, joinedload

from . import BASE, UUIDMixin, TimestampMixin


class BlogSubClass(BASE, UUIDMixin, TimestampMixin):
    """blog's class: used for classify"""
    __tablename__ = 'blog_subclasses'
    
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(100), nullable=True)
    protected = Column(Boolean, default=False)
    
    class_id = Column(String(32), ForeignKey('blog_classes.id'), nullable=False)
    # support lazy, joined, dynamic relationship loading
    blogs = relationship('Blog', backref=backref('subclass', lazy='joined'), 
        cascade='all, delete-orphan')
    blog_query = relationship('Blog', lazy='dynamic')

    @staticmethod
    def get_blog_subclasses(db_session, **kwargs):
        search = kwargs.pop('search', None)
        offset = kwargs.pop('offset', None)
        limit = kwargs.pop('limit', None)
        return_total = kwargs.pop('return_total', False)
        lazy = kwargs.pop('lazy', True)
        
        query = db_session.query(BlogSubClass)
        if return_total:
            total = query.count()
        if search is not None:
            query = query.filter(BlogSubClass.name.contains(search))
        
        query = query.order_by(BlogSubClass.updated_at.desc())
        if offset is not None:
            query = query.offset(offset)
        if limit is not None:
            query = query.limit(limit)
        if not lazy:
            query = query.options(joinedload(BlogSubClass.blogs))
            
        if return_total:
            # return items' total and display items
            return total, query.all()
        else:
            return query.all()

    @staticmethod
    def get_blog_subclass(db_session, *args, **kwargs):
        _id = args[0] if len(args) >= 1 else None
        if _id is not None:
            blog_subclass = db_session.query(BlogSubClass).filter(
                BlogSubClass.id == _id).first()
            return blog_subclass
        
        _name = kwargs.pop('name', None)
        if _name is not None:
            blog_subclass = db_session.query(BlogSubClass).filter(
                BlogSubClass.name == _name).first()
            return blog_subclass
        
        return None

    @staticmethod
    def delete_blog_subclass(db_session, subclass_id):
        """Delete blog subclass of specified ID"""
        blog_subclass = db_session.query(BlogSubClass).filter(
                BlogSubClass.id == subclass_id).first()
        if blog_subclass:
            db_session.delete(blog_subclass)
            db_session.commit()
        return blog_subclass

    @staticmethod
    def insert_blog_subclass(db_session, **kwargs):
        name = kwargs.pop('name')
        class_id = kwargs.pop('class_id')
        protected = kwargs.pop('protected', False)
        description = kwargs.pop('description', '')
        blog_subclass = BlogSubClass(name=name, description=description,
            protected=protected, class_id=class_id)
        db_session.add(blog_subclass)
        db_session.commit()
        return blog_subclass
