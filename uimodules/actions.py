# coding=utf-8
from tornado.web import UIModule


class Actions(UIModule):
    """Page Actions"""
    
    def render(self):
        return self.render_string('uimodules/actions.html')