# coding=utf-8
from tornado.web import UIModule


class NoticeBoard(UIModule):
    """Notice Board"""
    
    def render(self):
        return self.render_string('uimodules/notice_board.html')