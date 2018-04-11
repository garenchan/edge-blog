# coding=utf-8
import math

from tornado.web import RequestHandler
from tornado import gen

from . import BaseHandler
from models import BlogClass, BlogSubClass, Blog


class CommonBaseHandler(BaseHandler):

    @gen.coroutine
    def get_blog_classes(self):
        _blog_classes = yield self.async_do(BlogClass.get_blog_classes, 
            self.db_session, lazy=False)
        
        for _blog_class in _blog_classes[:]:
            for _blog_subclass in _blog_class.subclasses[:]:
                if _blog_subclass.protected:
                    _blog_class.subclasses.remove(_blog_subclass)
            if len(_blog_class.subclasses) == 0:
                _blog_classes.remove(_blog_class)
        return _blog_classes

    @gen.coroutine
    def prepare(self):
        yield super().prepare()
        self.blog_classes = yield self.get_blog_classes()

    def get_template_namespace(self):
        """
        NOTE: In the common pages, we need to genarate dynamic navbar,
        so we need to pass blog_classes variable repeatedly when render template!
        This is very inconvenient, we add it into template namespace and use it
        directly.
        """
        namespace = super().get_template_namespace()
        namespace['blog_classes'] = self.blog_classes
        return namespace


class DashboardView(CommonBaseHandler):

    @gen.coroutine
    def get(self):
        self.render('common/dashboard.html')


class BlogSubClassIndexView(CommonBaseHandler):
    
    BLOGS_PER_PAGE = 10
    
    @gen.coroutine
    def get_blogs(self, blog_query, page_id):
        total = yield self.async_do(blog_query.count)
        offset = (page_id - 1) * self.BLOGS_PER_PAGE
        blogs = yield self.async_do(
            blog_query.order_by(Blog.updated_at.desc()).
            offset(offset).
            limit(self.BLOGS_PER_PAGE).all)
        return blogs, total
    
    @gen.coroutine
    def get(self, subclass_id, page_id):
        blog_subclass = yield self.async_do(BlogSubClass.get_blog_subclass, 
                                            self.db_session, subclass_id)
        if not blog_subclass:
            self.write_error(404)
        else:
            try:
                page_id = int(page_id)
            except ValueError:
                page_id = 1
            print('page_id', page_id)
            blogs, total = yield self.get_blogs(blog_subclass.blog_query, 
                                                page_id)
            pages=math.ceil(total / self.BLOGS_PER_PAGE)
            
            self.render('common/blog_subclass_index.html', 
                        blogs=blogs,
                        pages=pages,
                        page=page_id,
                        subclass_name=blog_subclass.name,
                        class_name=blog_subclass.cls.name)


class BlogReaderView(CommonBaseHandler):
    
    @gen.coroutine
    def get_blog_content(self, blog):
        """ We defer the load of the blog's content,
            when we access a blog's content attribute,
            it will lead to a sql query and maybe block 
            tornado's main thread!
        """
        def get_content():
            return blog.content
        content = yield self.async_do(get_content)
        return content
    
    @gen.coroutine
    def get(self, blog_id):
        blog = yield self.async_do(Blog.get_blog, self.db_session, blog_id)
        print('blog_id', blog_id)
        if not blog:
            self.write_error(404)
        content = yield self.get_blog_content(blog)
        self.render('common/blog_reader.html', blog=blog)