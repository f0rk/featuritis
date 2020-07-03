class FeaturitisError(Exception):

    def __init__(self, message):
        self.message = message


class InitializationError(FeaturitisError):
    pass


class ConfigError(FeaturitisError):
    pass


class FeatureExistsError(FeaturitisError):
    pass
