# coding=utf-8
import json

from tornado.web import RequestHandler
from tornado import gen

from models.user import User
from models.blog_class import BlogClass


class BaseHandler(RequestHandler):

    def initialize(self):
        self.db_session = self.application.db_pool()
        self.async_do = self.application.thread_pool.submit
        # session related
        self.session = self.application.session_manager.make_session(self)
        self.session_remove_flag = False

    @gen.coroutine
    def prepare(self):
        """ NOTE: We need to get current_user in prepare(),
                because get_current_user() cannot be a coroutine!
        """
        user_id = yield self.session.get_user_id()
        if user_id:
            user = yield self.async_do(User.get_user_by_id, 
                self.db_session, user_id)
            if user:
                self.current_user = user

    def get_json_argument(self, name, *args):
        """Get json argument"""
        # TODO: We need to check whether the request's content-type is
        # application/json and get the charset.
        _json = getattr(self, '_json', None)
        if _json is None:
            body = self.request.body
            if isinstance(body, bytes):
                body = body.decode()
            _json = self._json = json.loads(body)
        try:
            value = _json[name]
        except KeyError:
            if len(args) >= 1:
                value = args[0]
            else:
                raise
        return value

    @gen.coroutine
    def login_user(self, user):
        self.session.generate_sessionid(user)
        yield self.session.save()

    def logout_user(self):
        self.session_remove_flag = True
        self.session.remove_sessionid()

    def write_error(self, status_code, **kwargs):
        if status_code == 404:
            self.render('errors/404.html')

    @gen.coroutine
    def on_finish(self):
        if self.db_session:
            self.db_session.close()
        if self.session_remove_flag:
            yield self.session.remove()

    @gen.coroutine
    def get_blog_classes(self):
        _blog_classes = yield self.async_do(BlogClass.get_blog_classes, 
            self.db_session)
        
        blog_classes = []
        for _blog_class in _blog_classes:
            if _blog_class.subclasses.count() <= 0:
                continue
            