# coding=utf-8
from tornado.web import RequestHandler

from . import BaseHandler


class DashboardView(BaseHandler):

    def get(self):
        self.render('dashboard.html')