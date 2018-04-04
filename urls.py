# coding=utf-8
from tornado.web import url

from views.dashboard import DashboardView
from views.auth import LoginHandler, LogoutHandler
from views.error import NotFoundErrorHandler

handlers = [
    # App
    url(r'/', DashboardView, name='main'),
    url(r'/dashboard', DashboardView, name='dashboard'),
    
    # Auth
    url(r'/auth/login', LoginHandler, name='login'),
    url(r'/auth/logout', LogoutHandler, name='logout'),
    
    # Error
    (r".*", NotFoundErrorHandler),
]