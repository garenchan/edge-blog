import time
from hashlib import sha1

from tornado import gen

from . import BaseSession, BaseSessionManager


class CookieSession(BaseSession):
    """ Use cookie as session store
    """

    def __init__(self, request_handler, session_manager):
        super().__init__(request_handler, session_manager)
        self.cookie_key = session_manager.COOKIE_KEY
        self.cookie_max_age = session_manager.COOKIE_MAX_AGE
        self.cookie_expires = session_manager.COOKIE_EXPIRES
        self.sessionid = None

    @staticmethod
    def _get_signature(*args):
        """Simple signature algorithm
           NOTE: may be necessary to use salt value
        """
        _sign = '-'.join(args)
        _sign = sha1(_sign.encode('utf-8')).hexdigest()
        return _sign

    def generate_sessionid(self, user):
        user_id = user.get_id()
        expires = str(int(time.time() + self.cookie_max_age))
        
        _sign = self._get_signature(user_id, expires)
        self.sessionid = '-'.join([user_id, expires, _sign])
        return self.sessionid

    @gen.coroutine
    def get_user_id(self):
        try:
            if not self.sessionid:
                self.sessionid = self.request_handler.get_secure_cookie(
                        self.cookie_key)
            if not self.sessionid:
                return None
            # NOTE: get_secure_cookie return bytes string if exist
            if isinstance(self.sessionid, bytes):
                self.sessionid = self.sessionid.decode()
            user_id, expires, sign = self.sessionid.split('-')[:3]
            
            # check whether expires
            if int(expires) < time.time():
                return None
            # check whether be tampered
            wish_sign = self._get_signature(user_id, expires)
            if wish_sign != sign:
                return None
        except:
            return None
        else:
            return user_id

    @gen.coroutine
    def save(self):
        if self.sessionid is None:
            raise ValueError('`sessionid` cannot be None')
        self.request_handler.set_secure_cookie(self.cookie_key, self.sessionid, 
                                               self.cookie_expires)

    @gen.coroutine
    def remove(self):
        """ noop here, but we can confirm that cookie is cleared """
        # self.request_handler.clear_cookie(self.cookie_key)


class CookieSessionManager(BaseSessionManager):
    """ Use to manage session configuraton and make session
    """
    
    def make_session(self, request_handler):
        return CookieSession(request_handler, self)