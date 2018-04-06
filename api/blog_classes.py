# coding=utf-8
import logging

from tornado.web import authenticated
from tornado import gen
from sqlalchemy.exc import IntegrityError

from views import BaseHandler
from models.blog_class import BlogClass


class BlogClassesAPI(BaseHandler):

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

    @authenticated
    @gen.coroutine
    def post(self):
        """ Create BlogClass
        Request Example
        {
            "blog_class": {
                "name": "Database",
                "description": "Database related"  --> optional
            }
        }
        Response Example
        {
            "blog_class": {
                "id": "ab06aabd94724ba3ae78db79e79420dc",
                "name": "Database",
                "description": ""Database related",
                "order": 5
            }
        }
        """
        name = self.get_argument('name')
        description = self.get_argument('description')

        try:
            # TODO: form validate here
            kwargs = dict(
                name=name,
                description=description
            )
            blog_class = yield self.async_do(BlogClass.insert_blog_class,
                self.db_session, **kwargs)
            # return response
            response = {
                'blog_class': {
                    'id': blog_class.id,
                    'name': blog_class.name,
                    'description': blog_class.description,
                    'order': blog_class.order
                }
            }
            self.set_status(201)
        except IntegrityError as ex:
            response = {
                'error': {
                    'status': 400,
                    'message': ex.orig.args[1],
                    'code': ex.orig.args[0],
                }
            }
            self.set_status(400)
        except Exception as ex :
            response = {
                'error': {
                    'status': 500,
                    'message': str(ex),
                    'code': None,
                }
            }
            self.set_status(500)
        finally:
            self.write(response)