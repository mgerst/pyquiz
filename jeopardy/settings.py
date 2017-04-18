class Config(object):
    SECRET_KEY = 'REPLACE_ME'
    ADMIN_PW = 'REPLACE_ME'


class ProdConfig(Config):
    ENV = 'prod'
    REDIS_DB = 2
    REDIS_HOST = "localhost"


class DevConfig(Config):
    ENV = 'dev'
    DEBUG = True
    DEBUT_TB_INTERCEPT_REDIRECTS = False

    ASSETS_DEBUG = True
    REDIS_DB = 2
    REDIS_HOST = "localhost"


class TestConfig(Config):
    ENV = 'test'
    DEBUG = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    REDIS_DB = 2
    REDIS_HOST = "localhost"
