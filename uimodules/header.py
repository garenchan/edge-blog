# coding=utf-8
from tornado.web import UIModule


class Header(UIModule):
    """Page Headr"""
    
    def render(self, page_title, page_title_second):
        return self.render_string('uimodules/header.html', 
            page_title=page_title, page_title_second=page_title_second)