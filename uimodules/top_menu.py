# coding=utf-8
from tornado.web import UIModule


class TopMenu(UIModule):
    """Top Menu"""
    
    def render(self):
        return self.render_string('uimodules/top_menu.html')