# coding=utf-8
import logging

from tornado.web import authenticated
from tornado import gen

from . import APIHandler
from models.blog import Blog


class BlogsAPI(APIHandler):


    @gen.coroutine
    def _datatable_ajax_source(self):
        COL_MAP = {
            '-1': 'updated_at',
            '0': 'title',
            '3': 'view_counter',
        }
        try:
            echo = self.get_argument('sEcho', '1')
            offset = int(self.get_argument('iDisplayStart', '0'))
            limit = int(self.get_argument('iDisplayLength', '10'))
            search = self.get_argument('sSearch', '')
            sortcol = self.get_argument('iSortCol_0', '-1')
            sortcol = COL_MAP.get(sortcol, 'updated_at')
            seq = self.get_argument('sSortDir_0', 'desc')
            order_by = (sortcol, seq)
        except ValueError:
            self.set_status(400)
            return self.make_error_response(400, 'Params error', None)
        
        try:
            kwargs = dict(search=search, offset=offset, 
                          limit=limit, order_by=order_by, return_total=True)
            total, _blogs = yield self.async_do(
            Blog.get_blogs, self.db_session, **kwargs)
        except ValueError:
            self.set_status(400)
            response = self.make_error_response(400, 'Params error', None)
        except Exception as ex:
            self.set_status(500)
            response = self.make_error_response(500,
                'Internal server error', None)
        else:
            response = dict(
                sEcho=echo,
                iTotalRecords=total,
                iTotalDisplayRecords=total,
                aaData=[]
            )
            for _blog in _blogs:
                response['aaData'].append(dict(
                    id=_blog.id,
                    title=_blog.title,
                    summary=_blog.summary,
                    content=_blog.content,
                    view_counter=_blog.view_counter,
                    subclass=_blog.subclass.name,
                    source=_blog.source.name,
                    updated_at=str(_blog.updated_at),
                    created_at=str(_blog.created_at)
                ))
        finally:
            return response

    @gen.coroutine
    def get_blog_by_id(self, _id):
        _blog = yield self.async_do(Blog.get_blog, self.db_session, _id)
        response = { 'blog': {} }
        if _blog:
            response['blog'] = dict(
                id=_blog.id,
                title=_blog.title,
                summary=_blog.summary,
                content=_blog.content,
                view_counter=_blog.view_counter,
                subclass=_blog.subclass.name,
                source=_blog.source.name,
                updated_at=str(_blog.updated_at),
                created_at=str(_blog.created_at)
            )
        return response

    @gen.coroutine
    def get_blogs(self):
        try:
            search = self.get_argument('search', '')
            offset = self.get_argument('offset', None)
            if offset:
                offset = int(offset)
            limit = self.get_argument('limit', None)
            if limit:
                limit = int(limit)
            # add sort params
            order_by = self.get_argument('order_by', 'updated_at')
            seq = self.get_argument('seq', 'desc')
            order_by = (order_by, seq)
        except ValueError:
            self.set_status(400)
            return self.make_error_response(400, 'Params error', None)
        
        try:
            kwargs = dict(search=search, offset=offset, limit=limit, 
                order_by=order_by)
            _blogs = yield self.async_do(
            Blog.get_blogs, self.db_session, **kwargs)
        except ValueError:
            self.set_status(400)
            response = self.make_error_response(400, 'Params error', None)
        except Exception as ex:
            self.set_status(500)
            response = self.make_error_response(500,
                'Internal server error', None)
        else:
            response = { 'blogs': [] }
            for _blog in _blogs:
                response['blogs'].append(dict(
                    id=_blog.id,
                    title=_blog.title,
                    summary=_blog.summary,
                    content=_blog.content,
                    view_counter=_blog.view_counter,
                    subclass=_blog.subclass.name,
                    source=_blog.source.name,
                    updated_at=str(_blog.updated_at),
                    created_at=str(_blog.created_at)
                ))
        finally:
            return response

    @authenticated
    @gen.coroutine
    def get(self, *args):
        if args:
            _id = args[0]
            response = yield self.get_blog_by_id(_id)
            return self.write(response)
        
        sEcho = self.get_argument('sEcho', None)
        if sEcho:
            response = yield self._datatable_ajax_source()
            return self.write(response)
        
        response = yield self.get_blogs()
        self.write(response)

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
                    'subclass': blog.subclass.name,
                    'created_at': str(blog.created_at)
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
        if not args:
            response = self.make_error_response(400, 
                'No blog id is specified', None)
            self.set_status(400)
            return self.write(response)
            
        try:
            _id = args[0]
            _blog = yield self.async_do(
                Blog.delete_blog, self.db_session, _id)
        except Exception as ex:
            response = self.make_error_response(500, str(ex), None)
            self.set_status(500)
        else:
            if _blog is None:
                # mean blog subclass not exists
                response = self.make_error_response(404, 
                    'Blog of id %r not found' % _id, None)
                self.set_status(404)
            else:
                response = None
                self.set_status(204)
        finally:
            if response:
                self.write(response)