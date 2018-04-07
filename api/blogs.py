# coding=utf-8
import logging

from tornado.web import authenticated
from tornado import gen

from . import APIHandler


class BlogsAPI(APIHandler):


    @authenticated
    @gen.coroutine
    def post(self):
        