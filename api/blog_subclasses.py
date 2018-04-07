# coding=utf-8
import logging

from tornado.web import authenticated, MissingArgumentError
from tornado import gen

from . import APIHandler
from models.blog_subclass import BlogSubClass


class BlogSubClassesAPI(APIHandler):

    @gen.coroutine
    def _datatable_ajax_source(self):
        echo = self.get_argument('sEcho', '1')
        offset = int(self.get_argument('iDisplayStart', '0'))
        limit = int(self.get_argument('iDisplayLength', '10'))
        search = self.get_argument('sSearch', '')
        
        kwargs = dict(search=search, offset=offset, 
                      limit=limit, return_total=True)
        total, _blog_subclasses = yield self.async_do(
            BlogSubClass.get_blog_subclasses, self.db_session, **kwargs)
        
        response = dict(
            sEcho=echo,
            iTotalRecords=total,
            iTotalDisplayRecords=total,
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

    @gen.coroutine
    def get_by_id(self, _id):
        """get subclass info of specified id
GET /api/blog_subclasses/ab06aabd94724ba3ae78db79e79420dc HTTP/1.1

Response Example
{
    "blog_subclass": {
        "id": "ab06aabd94724ba3ae78db79e79420dc",
        "name": "Database",
        "description": ""Database related",
        "protected": True,
        "cls": "DB"
    }
}
        """
        _blog_subclass = yield self.async_do(BlogSubClass.get_blog_subclass,
            self.db_session, _id)
        response = {
            'blog_subclass': {
            }
        }
        if _blog_subclass:
            response['blog_subclass'] = {
                'id': _blog_subclass.id,
                'name': _blog_subclass.name,
                'description': _blog_subclass.description,
                'protected': _blog_subclass.protected,
                'cls': _blog_subclass.cls.name
            }
        return response

    @authenticated
    @gen.coroutine
    def get(self, *args):
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
        if args:
            # mean get subclass info of specified id
            _id = args[0]
            response = yield self.get_by_id(_id)
            return self.write(response)
            
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
        """ Create BlogSubClass
Request Example
{
    "blog_subclass": {
        "name": "Database",
        "class_id": "db06aabd94ef4ba3ae78db79e79420dc",
        "protected": True,                 --> optional, default:False
        "description": "Database related"  --> optional
    }
}
Response Example
{
    "blog_subclass": {
        "id": "ab06aabd94724ba3ae78db79e79420dc",
        "name": "Database",
        "description": ""Database related",
        "protected": True,
        "cls": "DB"
    }
}
        """
        try:
            blog_subclass_dict = self.get_json_argument('blog_subclass')
            name = blog_subclass_dict['name']
            class_id = blog_subclass_dict['class_id']
            protected = blog_subclass_dict.get('protected', False)
            description = blog_subclass_dict.get('description', '')
        except (MissingArgumentError, KeyError) as ex:
            if isinstance(ex, MissingArgumentError):
                message = ex.log_message
            elif isinstance(ex, KeyError):
                message = 'Missing argument %s' % ex.args[0]
            response = self.make_error_response(400, message, None)
            self.set_status(400)
            return self.write(response)

        try:
            # TODO: form validate here
            kwargs = dict(
                name=name,
                class_id=class_id,
                protected=protected,
                description=description
            )
            blog_subclass = yield self.async_do(
                BlogSubClass.insert_blog_subclass, self.db_session, **kwargs)
            # return response
            response = {
                'blog_subclass': {
                    'id': blog_subclass.id,
                    'name': blog_subclass.name,
                    'description': blog_subclass.description,
                    'protected': blog_subclass.protected,
                    'cls': blog_subclass.cls.name
                }
            }
            self.set_status(201)
        except IntegrityError as ex:
            # When name is existed, raise duplicate error;
            # When class_id isn't existed, raise foreign key constraint error
            response = self.make_error_response(400, ex.orig.args[1][:64], 
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
        """delete blog subclass of specified id.
DELETE /api/blog_subclasses/ab06aabd94724ba3ae78db79e79420dc HTTP/1.1

Response Example
There is no body content for the response of a successful DELETE request.
        """
        if not args:
            response = self.make_error_response(400, 
                'No blog subclass id is specified', None)
            self.set_status(400)
            return self.write(response)
            
        try:
            _id = args[0]
            _blog_subclass = yield self.async_do(
                BlogSubClass.delete_blog_subclass, self.db_session, _id)
        except Exception as ex:
            response = self.make_error_response(500, str(ex), None)
            self.set_status(500)
        else:
            if _blog_subclass is None:
                # mean blog subclass not exists
                response = self.make_error_response(404, 
                    'Blog subclass of id %r not found' % _id, None)
                self.set_status(404)
            else:
                response = None
                self.set_status(204)
        finally:
            if response:
                self.write(response)