import redis


class Config(object):
    SECRET_KEY = 'REPLACE_ME'
    ADMIN_PW = 'REPLACE_ME'
    SESSION_TYPE = 'redis'
    SESSION_REDIS = redis.StrictRedis(host='localhost', db=2)


class ProdConfig(Config):
    ENV = 'prod'
    REDIS_DB = 2
    REDIS_HOST = "localhost"
    WEBPACK_MANIFEST_PATH = '../manifest.prod.json'


class DockerConfig(ProdConfig):
    REDIS_DB = 1
    REDIS_HOST = "redis"
    SESSION_REDIS = redis.StrictRedis(host='redis', db=2)


class DevConfig(Config):
    ENV = 'dev'
    DEBUG = True
    DEBUT_TB_INTERCEPT_REDIRECTS = False
    WEBPACK_MANIFEST_PATH = '../manifest.dev.json'

    ASSETS_DEBUG = True
    REDIS_DB = 2
    REDIS_HOST = "localhost"


class TestConfig(Config):
    ENV = 'test'
    DEBUG = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    REDIS_DB = 2
    REDIS_HOST = "localhost"
    WEBPACK_MANIFEST_PATH = '../manifest.prod.json'

