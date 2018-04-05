# coding=utf-8
import logging
import os
from concurrent.futures.thread import ThreadPoolExecutor

import tornado.web
from tornado.ioloop import IOLoop
import alembic.config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from urls import handlers
from contrib import cli
from contrib.session.cookie import CookieSessionManager
import configs

from models.user import User
from models.blog_source import BlogSource
from models.blog_class import BlogClass

logger = logging.getLogger(__name__)
manager = cli.CLI(prog='EdgeBlog', version='1.0.0')


@manager.command(description='Upgrade Database')
def upgrade():
    alembic.config.main('upgrade head'.split(' '), 'alembic')


@manager.command(description='Init Database Data')
def deploy():
    engine = create_engine(configs.DB.engine_url)
    DBSession = sessionmaker(bind=engine, autocommit=False)
    session = DBSession()
    User.insert_default_user(session)
    BlogSource.insert_default_sources(session)
    BlogClass.insert_default_classes(session)
    session.close()


class Application(tornado.web.Application):
    
    def __init__(self, **kwargs):
        kwargs.update(handlers=handlers)
        super(Application, self).__init__(**kwargs)
        self.db_engine = create_engine(configs.DB.engine_url, **configs.DB.engine_settings)
        self.db_pool = sessionmaker(bind=self.db_engine, autocommit=False)
        self.thread_pool = ThreadPoolExecutor(10)
        self.session_manager = CookieSessionManager(**configs.SESSION)


@manager.option('-p', '--port', type=int, default=8888)
@manager.option('-H', '--host', default='0.0.0.0')
def runserver(host, port):
        app = Application(**configs.APP)
        app.listen(port, address=host)
        IOLoop.current().start()


if __name__ == '__main__':
    manager.run()