# coding=utf-8
from tornado.web import authenticated

from . import BaseHandler


class AdminDashboardHandler(BaseHandler):
    """Administrator's dashboard"""

    @authenticated
    def get(self):
        self.render('admin/dashboard.html')


class PostBlogHandler(BaseHandler):
    """Post new blog"""

    @authenticated
    def get(self):
        self.render('admin/post_blog.html')


class BlogClassHandler(BaseHandler):
    """Blog classification management"""

    @authenticated
    def get(self):
        self.render('admin/blog_class.html')


class ManageBlogsHandler(BaseHandler):
    """Manage posted blogs"""
    
    @authenticated
    def get(self):
        self.render('admin/manage_blogs.html')