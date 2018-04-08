# coding=utf-8
from tornado import gen

from . import BaseHandler
from models.blog_class import BlogClass


class TestHandler(BaseHandler):


    @gen.coroutine
    def get(self):
        blog_classes = yield self.async_do(BlogClass.get_blog_classes, self.db_session)
        blog_classes = [i for i in blog_classes if i.subclasses.count() > 0]
        self.render('test.html', blog_classes=blog_classes)