class Config(object):
    SECRET_KEY = 'REPLACE_ME'


class ProdConfig(Config):
    ENV = 'prod'


class DevConfig(Config):
    ENV = 'dev'
    DEBUG = True
    DEBUT_TB_INTERCEPT_REDIRECTS = False

    ASSETS_DEBUG = True


class TestConfig(Config):
    ENV = 'test'
    DEBUG = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
