# coding=utf-8
import logging

from tornado.web import authenticated
from tornado import gen

from . import APIHandler
from models.blog import Blog


class BlogsAPI(APIHandler):


    @authenticated
    @gen.coroutine
    def post(self):
        try:
            blog_dict = self.get_json_argument('blog')
            title = blog_dict['title'].strip()
            source_id = blog_dict['source_id'].strip()
            subclass_id = blog_dict['subclass_id'].strip()
            summary = blog_dict['summary'].strip()
            content = blog_dict['content']
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
                title=title,
                summary=summary,
                content=content,
                source_id=source_id,
                subclass_id=subclass_id
            )
            blog = yield self.async_do(
                Blog.insert_blog, self.db_session, **kwargs)
            # return response
            response = {
                'blog': {
                    'id': blog.id,
                    'title': blog.title,
                    'summary': blog.summary,
                    'content': blog.content,
                    'source': blog.source.name,
                    'subclass': blog.subclass.name
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