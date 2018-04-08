# coding=utf-8
from tornado.web import UIModule

from models.blog_class import BlogClass


class Navbar(UIModule):
    """Common Navbar"""
    
    def render(self, blog_classes):
        return self.render_string('uimodules/navbar.html', 
            blog_classes=blog_classes)