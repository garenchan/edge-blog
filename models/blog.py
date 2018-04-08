# coding=utf-8
from sqlalchemy import Column, String, Text, Integer, ForeignKey
from sqlalchemy import or_
from sqlalchemy.orm import deferred
from sqlalchemy.orm.attributes import InstrumentedAttribute

from . import BASE, UUIDMixin, TimestampMixin


class Blog(BASE, UUIDMixin, TimestampMixin):
    __tablename__ = 'blogs'
    
    title = Column(String(50), nullable=False)
    summary = Column(String(200), nullable=True)
    content = deferred(Column(Text, nullable=False))
    view_counter = Column(Integer, default=0)
    
    source_id = Column(String(32), ForeignKey('blog_sources.id'),
        nullable=False)
    subclass_id = Column(String(32), ForeignKey('blog_subclasses.id'),
        nullable=False)

    @staticmethod
    def get_blog(db_session, *args, **kwargs):
        _id = args[0] if len(args) >= 1 else None
        if _id is not None:
            blog = db_session.query(Blog).filter(Blog.id == _id).first()
            return blog
        
        _title = kwargs.pop('title', None)
        if _title:
            blog = db_session.query(Blog).filter(Blog.title == _title).first()
            return blog
        
        return None

    @staticmethod
    def get_blogs(db_session, **kwargs):
        search = kwargs.pop('search', None)
        offset = kwargs.pop('offset', None)
        limit = kwargs.pop('limit', None)
        return_total = kwargs.pop('return_total', False)
        # order by [___] desc/asc
        order_by, seq = kwargs.pop('order_by', (None, None))
        if order_by is None:
            order_by = 'updated_at'
        if seq is None:
            seq = 'desc'
        order_by = getattr(Blog, order_by, None)
        if order_by is None or not isinstance(order_by, InstrumentedAttribute):
            raise ValueError('Unknown order_by field %r' % order_by)
        if seq.lower() not in ['desc', 'asc']:
            raise ValueError('Unknown order_by rule %r' % seq)
        else:
            order_by = getattr(order_by, seq.lower())()
        
        query = db_session.query(Blog)
        if return_total:
            total = query.count()
        
        if search is not None:
            query = query.filter(or_(Blog.title.contains(search), 
                Blog.summary.contains(search)))
                
        query = query.order_by(order_by)
        if offset is not None:
            query = query.offset(offset)
        if limit is not None:
            query = query.limit(limit)
            
        if return_total:
            return total, query.all()
        else:
            return query.all()

    @staticmethod
    def insert_blog(db_session, **kwargs):
        title = kwargs.pop('title')
        summary = kwargs.pop('summary', '')
        content = kwargs.pop('content')
        source_id = kwargs.pop('source_id')
        subclass_id = kwargs.pop('subclass_id')
        blog = Blog(title=title, summary=summary, content=content,
            source_id=source_id, subclass_id=subclass_id)
        db_session.add(blog)
        db_session.commit()
        return blog

    @staticmethod
    def delete_blog(db_session, blog_id):
        blog = db_session.query(Blog).filter(
                Blog.id == blog_id).first()
        if blog:
            db_session.delete(blog)
            db_session.commit()
        return blog