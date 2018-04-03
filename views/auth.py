# coding=utf-8
from tornado import gen

from . import BaseHandler
from model.models import User

class LoginHandler(BaseHandler):

    def get(self):
        self.render('auth/login.html')
    
    @gen.coroutine
    def post(self):
        username = self.get_argument('username')
        password = self.get_argument('password')
        next_url = self.get_argument('next', '/')
        if not username or not password:
            self.write(dict(
                success=False,
                error='用户名或密码不能为空!',
            ))
            return
            
        user = yield self.async_do(User.get_user, self.db_session, username)
        if not user:
            self.write(dict(
                success=False,
                error='用户名或邮箱不存在!',
            ))
        elif user.verify_password(password):
            self.redirect(next_url)
        else:
            self.write(dict(
                success=False,
                error='用户名或密码不正确!',
            ))