# coding=utf-8
from sqlalchemy import Column, String, Text, Integer, ForeignKey

from . import BASE, UUIDMixin, TimestampMixin


class Blog(BASE, UUIDMixin, TimestampMixin):
    __tablename__ = 'blogs'
    
    title = Column(String(50), nullable=False)
    summary = Column(String(200), nullable=True)
    content = Column(Text, nullable=False)
    view_counter = Column(Integer, default=0)
    
    source_id = Column(String(32), ForeignKey('blog_sources.id'),
        nullable=False)
    subclass_id = Column(String(32), ForeignKey('blog_subclasses.id'),
        nullable=False)