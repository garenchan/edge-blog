# coding=utf-8
from tornado.web import RequestHandler


class DashboardView(RequestHandler):

    def get(self):
        self.render('dashboard.html')