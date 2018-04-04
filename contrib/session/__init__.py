# coding=utf-8
from abc import ABC, abstractmethod

from tornado import gen


class UserMixin(object):
    """This provides default implementations for the methods
    expects user objects to have.
    """
    
    def get_id(self):
        try:
            return str(self.id)
        except AttributeError:
            raise NotImplementedError('No `id` attribute - override `get_id`')

    def get_password(self):
        try:
            return str(self.password)
        except AttributeError:
            raise NotImplementedError('No `password` attribute - override `get_password`')


class BaseSession(ABC):

    def __init__(self, request_handler, session_manager):
        self.request_handler = request_handler
        self.session_manager = session_manager

    @abstractmethod
    def generate_sessionid(self):
        """Generate session id"""

    @abstractmethod
    @gen.coroutine
    def get_user_id(self):
        """Get user id of current session
           NOTE: We can store session in DB or Cache like Memcached,
                so the step to get user id need to be async.
        """

    @abstractmethod
    @gen.coroutine
    def save(self):
        """Persistent session"""

    # NOTE: two stage delete
    def remove_sessionid(self):
        """ First stage, just remove cookie"""
        cookie_key = self.session_manager.COOKIE_KEY
        self.request_handler.clear_cookie(cookie_key)

    @abstractmethod
    @gen.coroutine
    def remove(self):
        """ Second stage, remove session in store backend"""


class BaseSessionManager(ABC):

    def __init__(self, **kwargs):
        self.COOKIE_KEY = kwargs.pop('cookie_key', 'session')
        self.COOKIE_MAX_AGE = kwargs.pop('max_age', 7200)
        self.COOKIE_EXPIRES = kwargs.pop('expires', None)

    @abstractmethod
    def make_session(self):
        """make a new session"""