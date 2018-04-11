# coding=utf-8
from tornado.web import url

from views.common import DashboardView, BlogSubClassIndexView, BlogReaderView
from views.auth import LoginHandler, LogoutHandler
from views.error import NotFoundErrorHandler
from views import admin
from views.test import TestHandler

from api.blog_classes import BlogClassesAPI
from api.blog_subclasses import BlogSubClassesAPI
from api.blog_sources import BlogSourcesAPI
from api.blogs import BlogsAPI


handlers = [
    # Common
    url(r'/', DashboardView, name='main'),
    url(r'/dashboard', DashboardView, name='dashboard'),
    url(r'/subclass/(?P<subclass_id>[^/]*)/(?P<page_id>[^/]*)', 
        BlogSubClassIndexView, name='subclass_index'),
    url(r'/blog/(?P<blog_id>[^/]*)', BlogReaderView, name='blog_reader'),
    
    # Auth
    url(r'/auth/login', LoginHandler, name='login'),
    url(r'/auth/logout', LogoutHandler, name='logout'),
    
    # Admin
    url(r'/admin/?', admin.AdminDashboardHandler, name='admin'),
    url(r'/admin/blog/post', admin.PostBlogHandler, name='post_blog'),
    url(r'/admin/blog/class', admin.BlogClassHandler, name='post_class'),
    url(r'/admin/blogs/manage', admin.ManageBlogsHandler, name='manage_blogs'),
    
    # API
    url(r'/api/blog_classes[/]?', BlogClassesAPI),
    url(r'/api/blog_classes/([^/]*)', BlogClassesAPI),
    url(r'/api/blog_subclasses[/]?', BlogSubClassesAPI),
    url(r'/api/blog_subclasses/([^/]*)', BlogSubClassesAPI),
    url(r'/api/blog_sources[/]?', BlogSourcesAPI),
    url(r'/api/blog_sources/([^/]*)', BlogSourcesAPI),
    url(r'/api/blogs[/]?', BlogsAPI),
    url(r'/api/blogs/([^/]*)', BlogsAPI),
    
    # Error
    (r'/test', TestHandler),
    (r'.*', NotFoundErrorHandler),
    
]