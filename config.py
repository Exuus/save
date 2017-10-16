class Config(object):
    """
        Common configurations
    """

    SECRET_KEY = 'p9Bv<3Eid9%$i01'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = '465'
    MAIL_USERNAME = 'noreply@getsave.io'
    MAIL_PASSWORD = 'getsave.io@2018'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    # Put any configurations here that are common across all environments


class DevelopmentConfig(Config):
    """
    Development configurations
    """

    SQLALCHEMY_DATABASE_URI = 'postgresql://muhireremy:8@localhost/save_dev'
    DEBUG = True
    SQLALCHEMY_ECHO = True


class TestConfig(Config):
    """
    Test Configurations
    """

    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:129083save909@localhost/save_test'
    SQLALCHEMY_ECHO = True
    DEBUG = True


class ProductionConfig(Config):
    """
    Production configurations
    """

    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:no_pass@localhost/save_prod'


app_config = {
    'development': DevelopmentConfig,
    'test': TestConfig,
    'production': ProductionConfig
}
