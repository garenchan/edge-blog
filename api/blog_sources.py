# coding=utf-8
import logging

from tornado.web import authenticated
from tornado import gen

from . import APIHandler
from models.blog_source import BlogSource


class BlogSourcesAPI(APIHandler):


    @authenticated
    @gen.coroutine
    def get(self):
        """List BlogSource"""
        try:
            search = self.get_argument('search', '')
            offset = self.get_argument('offset', None)
            if offset:
                offset = int(offset)
            limit = self.get_argument('limit', None)
            if limit:
                limit = int(limit)
        except Exception as ex:
            response = self.make_error_response(400, 'Params error', None)
            self.set_status(400)
            return self.write(response)
        # query in database
        try:
            kwargs = dict(search=search, offset=offset, limit=limit, lazy=False)
            _blog_sources = yield self.async_do(BlogSource.get_blog_sources, 
                self.db_session, **kwargs)
        except Exception as ex:
            logging.exception('A error raise when get_blog_sources')
            response = self.make_error_response(500,
                'Internal server error', None)
            self.set_status(500)
        else:
            response = { 'blog_sources': [] }
            for _blog_source in _blog_sources:
                response['blog_sources'].append(dict(
                    id=_blog_source.id,
                    name=_blog_source.name,
                    blog_num=len(_blog_source.blogs)
                ))
        finally:
            self.write(response)