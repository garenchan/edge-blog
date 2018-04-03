# coding=utf-8
import tornado.web

from . import BaseHandler


class NotFoundErrorHandler(BaseHandler):

    def get(self):
        raise tornado.web.HTTPError(404)

    def post(self):
        raise tornado.web.HTTPError(404)
