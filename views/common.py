# coding=utf-8
from tornado.web import RequestHandler
from tornado import gen

from . import BaseHandler
from models.blog_class import BlogClass

class DashboardView(BaseHandler):

    @gen.coroutine
    def get(self):
        blog_classes = yield self.async_do(BlogClass.get_blog_classes, self.db_session, joined=True)
        blog_classes = [i for i in blog_classes if len(i.subclasses) > 0]
        self.render('common/dashboard.html', blog_classes=blog_classes)