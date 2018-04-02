# coding=utf-8
import logging
import os

import tornado.web
from tornado.ioloop import IOLoop

from urls import handlers

logger = logging.getLogger(__name__)


class EdgeBlog(tornado.web.Application):
    
    def __init__(self, **kwargs):
        kwargs.update(handlers=handlers)
        super(EdgeBlog, self).__init__(**kwargs)
        

if __name__ == '__main__':
    CUR_DIR = os.path.dirname(__file__)
    settings = dict(
        template_path=os.path.join(CUR_DIR, 'templates'),
        static_path=os.path.join(CUR_DIR, 'static'),
        debug=True
    )
    app = EdgeBlog(**settings)
    app.listen(8888)
    IOLoop.current().start()