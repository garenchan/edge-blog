# coding=utf-8
import os

class Config(dict):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def __getattr__(self, attr):
        try:
            return self[attr]
        except KeyError:
            return None

### Database Configuration ###
DB = Config(
    engine_url='mysql+pymysql://root:admin123@172.18.231.151:3306/edge_blog?charset=utf8',
    engine_settings=Config(
        pool_recycle=3600,
        pool_timeout=30,
        pool_size=100,
        max_overflow=10
    ),
)

### Web App Configuration ###
CUR_DIR = os.path.dirname(__file__)

APP = Config(
    template_path=os.path.join(CUR_DIR, 'templates'),
    static_path=os.path.join(CUR_DIR, 'static'),
    login_url='/auth/login',
    cookie_secret='61oETzKXQAGaYdghdhgfhfhfg',
    xsrf_cookies=True,
    debug=True,
)

### Session Configuration ###
SESSION = Config(
    cookie_key='_XSESSION_',
    expires=1,
    max_age=3600,
)