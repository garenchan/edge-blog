# coding=utf-8
import logging

from tornado.web import authenticated
from tornado import gen

from views import BaseHandler
from models.blog_subclass import BlogSubClass


class ListBlogSubClasses(BaseHandler):

    @gen.coroutine
    def _datatable_ajax_source(self):
        echo = self.get_argument('sEcho', '1')
        offset = int(self.get_argument('iDisplayStart', '0'))
        limit = int(self.get_argument('iDisplayLength', '10'))
        search = self.get_argument('sSearch', '')
        
        kwargs = dict(search=search, offset=offset, limit=limit)
        _blog_subclasses = yield self.async_do(BlogSubClass.get_blog_subclasses, 
            self.db_session, **kwargs)
        
        response = dict(
            sEcho=echo,
            iTotalRecords=str(len(_blog_subclasses)),
            iTotalDisplayRecords=str(len(_blog_subclasses)),
            aaData=[]
        )
        for _blog_subclass in _blog_subclasses:
            response['aaData'].append(dict(
                id=_blog_subclass.id,
                name=_blog_subclass.name,
                description=_blog_subclass.description,
                protected=_blog_subclass.protected,
                cls=_blog_subclass.cls.name,
                blogs_num=_blog_subclass.blogs.count()
            ))
        return response

    @authenticated
    @gen.coroutine
    def get(self):
        """
GET /api/blog_subclasses HTTP/1.1

HTTP/1.1 200 OK
[
    {
        'id': 'd63271df8fc94e5fa82b7532f05f59a6',
        'name': 'MYSQL',
        'description': 'MYSQL存储引擎学习',
        'cls': '数据库',
        'blogs_num': 10,
        'protected': False
    },
    {
        'id': '18a7fdf74c374ca88eadca692ac8ae43',
        'name': 'NGINX',
        'description': 'NGINX WEB服务器',
        'cls': '后端',
        'blogs_num': 5,
        'protected': True
    }
]
        """
        sEcho = self.get_argument('sEcho', None)
        if sEcho:
            # means datatables load data from ajax
            response = yield self._datatable_ajax_source()
        else:
            response = {}
        self.write(response)