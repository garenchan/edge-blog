# coding=utf-8
import logging
import os

import tornado.web
from tornado.ioloop import IOLoop
import alembic.config

from urls import handlers
from utils import cli
from model import models
import config

logger = logging.getLogger(__name__)
manager = cli.CLI(prog='EdgeBlog', version='1.0.0')


@manager.command(description='Upgrade Database')
def upgrade():
    alembic.config.main('upgrade head'.split(' '), 'alembic')


class EdgeBlog(tornado.web.Application):
    
    def __init__(self, **kwargs):
        kwargs.update(handlers=handlers)
        super(EdgeBlog, self).__init__(**kwargs)

@manager.option('-p', '--port', type=int, default=8888)
@manager.option('-H', '--host', default='0.0.0.0')
def runserver(host, port):
        app = EdgeBlog(**config.APP)
        app.listen(port, address=host)
        IOLoop.current().start()

if __name__ == '__main__':
    manager.run()