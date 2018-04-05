# coding=utf-8
import logging

from tornado.web import authenticated
from tornado import gen

from views import BaseHandler
from models.blog_class import BlogClass


class ListBlogClasses(BaseHandler):

    @gen.coroutine
    def _datatable_ajax_source(self):
        echo = self.get_argument('sEcho', '1')
        offset = int(self.get_argument('iDisplayStart', '0'))
        limit = int(self.get_argument('iDisplayLength', '10'))
        search = self.get_argument('sSearch', '')
        
        kwargs = dict(search=search, offset=offset, limit=limit)
        _blog_classes = yield self.async_do(BlogClass.get_blog_classes, 
            self.db_session, **kwargs)
        
        response = dict(
            sEcho=echo,
            iTotalRecords=str(len(_blog_classes)),
            iTotalDisplayRecords=str(len(_blog_classes)),
            aaData=[]
        )
        for _blog_class in _blog_classes:
            response['aaData'].append(dict(
                id=_blog_class.id,
                name=_blog_class.name,
                description=_blog_class.description,
                order=_blog_class.order,
                subclasses=[sub.name for sub in _blog_class.subclasses.all()]
            ))
        return response

    @authenticated
    @gen.coroutine
    def get(self):
        """
GET /api/blog_classes HTTP/1.1

HTTP/1.1 200 OK
[
    {
        'id': 'd63271df8fc94e5fa82b7532f05f59a6',
        'name': '数据库',
        'description': '数据库知识',
        'subclasses': [{}, {}],
    },
    {
        'id': '18a7fdf74c374ca88eadca692ac8ae43',
        'name': '前端',
        'description': '前端知识',
        'subclasses': [{}, {}],
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