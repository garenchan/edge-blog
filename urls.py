# coding=utf-8
from tornado.web import url

from views.dashboard import DashboardView


handlers = [
    # App
    url(r'/', DashboardView, name='main'),
    url(r'/dashboard', DashboardView, name='dashboard'),
]