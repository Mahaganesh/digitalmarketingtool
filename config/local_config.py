from config.base_config import BaseConfig

class Configuration(BaseConfig):
    DEBUG = True

    POSTGRES = {
    'user': 'postgres',
    'pw': '080797', 
    'db': 'digitalmarketingtool',
    'host': 'localhost',
    'port': '5432',
    'ssl': ''
    }

    DB_URL = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s?ssl_key=%(ssl)s' % POSTGRES
