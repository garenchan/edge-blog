# coding=utf-8
from tornado.web import RequestHandler


class BaseHandler(RequestHandler):

    def initialize(self):
        self.db_session = self.application.db_pool()
        self.async_do = self.application.thread_pool.submit

    def prepare(self):
        pass

    def write_error(self, status_code, **kwargs):
        if status_code == 404:
            self.render('errors/404.html')
    
    def on_finish(self):
        if self.db_session:
            self.db_session.close()