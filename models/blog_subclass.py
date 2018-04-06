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

    @staticmethod
    def get_blog_subclasses(db_session, **kwargs):
        search = kwargs.pop('search', None)
        offset = kwargs.pop('offset', None)
        limit = kwargs.pop('limit', None)
        
        query = db_session.query(BlogSubClass)
        if search is not None:
            query = query.filter(BlogSubClass.name.contains(search))
        
        query = query.order_by(BlogSubClass.updated_at.desc())
        if offset is not None:
            query = query.offset(offset)
        if limit is not None:
            query = query.limit(limit)
            
        return query.all()

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
