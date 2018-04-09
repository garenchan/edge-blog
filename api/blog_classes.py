# coding=utf-8
import logging

from tornado.web import authenticated
from tornado import gen
from sqlalchemy.exc import IntegrityError

from . import APIHandler
from models.blog_class import BlogClass


class BlogClassesAPI(APIHandler):

    @gen.coroutine
    def _datatable_ajax_source(self):
        echo = self.get_argument('sEcho', '1')
        offset = int(self.get_argument('iDisplayStart', '0'))
        limit = int(self.get_argument('iDisplayLength', '10'))
        search = self.get_argument('sSearch', '')
        
        kwargs = dict(search=search, offset=offset, 
                      limit=limit, return_total=True, lazy=False)
        total, _blog_classes = yield self.async_do(BlogClass.get_blog_classes, 
            self.db_session, **kwargs)
        
        response = dict(
            sEcho=echo,
            iTotalRecords=total,
            iTotalDisplayRecords=total,
            aaData=[]
        )
        for _blog_class in _blog_classes:
            response['aaData'].append(dict(
                id=_blog_class.id,
                name=_blog_class.name,
                description=_blog_class.description,
                order=_blog_class.order,
                subclasses=[sub.name for sub in _blog_class.subclasses]
            ))
        return response

    @authenticated
    @gen.coroutine
    def get(self, *args):
        """ List BlogClass
GET /api/blog_classes HTTP/1.1

HTTP/1.1 200 OK
{
    'blog_classes': [
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
}
        """
        sEcho = self.get_argument('sEcho', None)
        if sEcho:
            # means datatables load data from ajax
            response = yield self._datatable_ajax_source()
            return self.write(response)
            
        try:
            search = self.get_argument('search', '')
            offset = self.get_argument('offset', None)
            if offset:
                offset = int(offset)
            limit = self.get_argument('limit', None)
            if limit:
                limit = int(limit)
        except Exception as ex:
            # params error
            response = self.make_error_response(400, 'Params error', None)
            self.set_status(400)
            return self.write(response)
        # query in database
        try:
            kwargs = dict(search=search, offset=offset, limit=limit,
                lazy=False)
            _blog_classes = yield self.async_do(BlogClass.get_blog_classes, 
                self.db_session, **kwargs)
        except Exception as ex:
            logging.exception('A error raise when get_blog_classes')
            response = self.make_error_response(500,
                'Internal server error', None)
            self.set_status(500)
        else:
            response = { 'blog_classes': [] }
            for cls in _blog_classes:
                response['blog_classes'].append(dict(
                    id=cls.id,
                    name=cls.name,
                    description=cls.description,
                    order=cls.order,
                    subclasses=[sub.name for sub in cls.subclasses]
                ))
        finally:
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
        name = self.get_argument('name', None)
        description = self.get_argument('description', '')

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
            response = self.make_error_response(400, ex.orig.args[1],
                ex.orig.args[0])
            self.set_status(400)
        except Exception as ex :
            response = self.make_error_response(500, str(ex), None)
            self.set_status(500)
        finally:
            self.write(response)

    @authenticated
    @gen.coroutine
    def delete(self, *args):
        """delete blog class of specified id.
DELETE /api/blog_classes/ab06aabd94724ba3ae78db79e79420dc HTTP/1.1

Response Example
There is no body content for the response of a successful DELETE request.
        """
        if not args:
            response = self.make_error_response(400, 
                'No blog class id is specified', None)
            self.set_status(400)
            return self.write(response)
            
        try:
            _id = args[0]
            _blog_class = yield self.async_do(
                BlogClass.delete_blog_class, self.db_session, _id)
        except Exception as ex:
            response = self.make_error_response(500, str(ex), None)
            self.set_status(500)
        else:
            if _blog_class is None:
                # mean blog class not exists
                response = self.make_error_response(404, 
                    'Blog class of id %r not found' % _id, None)
                self.set_status(404)
            else:
                response = None
                self.set_status(204)
        finally:
            if response:
                self.write(response)