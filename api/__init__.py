""" RESTful API
NOTE: 
    1. use http status to indicate success or failure of the operation
"""
from views import BaseHandler


class APIHandler(BaseHandler):
    """RESTful API base handler"""

    @staticmethod
    def make_error_response(status, message, code=None):
        return {
            'error': {
                'status': status,
                'message': message,
                'code': code,
            }
        }