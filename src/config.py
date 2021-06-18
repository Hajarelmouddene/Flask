# define environment-specific config variables
# Use classes and inheritance for multiple configurations.

class BaseConfig:
    TESTING = False


class DevelopmentConfig(BaseConfig):
    pass


class TestingConfig(BaseConfig):
    TESTING = True


class ProductionConfig(BaseConfig):
    pass
