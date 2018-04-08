# coding=utf-8
from tornado.web import UIModule


class AdminNavbar(UIModule):
    """Admin's Navbar"""
    
    def render(self):
        return self.render_string('uimodules/admin_navbar.html')