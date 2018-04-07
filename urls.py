# coding=utf-8
from tornado.web import url

from views.dashboard import DashboardView
from views.auth import LoginHandler, LogoutHandler
from views.error import NotFoundErrorHandler
from views import admin

from api.blog_classes import BlogClassesAPI
from api.blog_subclasses import BlogSubClassesAPI

handlers = [
    # App
    url(r'/', DashboardView, name='main'),
    url(r'/dashboard', DashboardView, name='dashboard'),
    
    # Auth
    url(r'/auth/login', LoginHandler, name='login'),
    url(r'/auth/logout', LogoutHandler, name='logout'),
    
    # Admin
    url(r'/admin/?', admin.AdminDashboardHandler, name='admin'),
    url(r'/admin/blog/post', admin.PostBlogHandler, name='post_blog'),
    url(r'/admin/blog/class', admin.BlogClassHandler, name='post_class'),
    
    # API
    url(r'/api/blog_classes[/]?', BlogClassesAPI),
    url(r'/api/blog_classes/([^/]*)', BlogClassesAPI),
    
    url(r'/api/blog_subclasses[/]?', BlogSubClassesAPI),
    url(r'/api/blog_subclasses/([^/]*)', BlogSubClassesAPI),
    
    # Error
    (r".*", NotFoundErrorHandler),
]