"""
Contains decorators that check if a feature has been enabled or not
"""

from dataall.core.config import config
from dataall.core.permission_checker import _process_func


def is_feature_enabled(config_property: str):
    def decorator(f):
        fn, fn_decorator = _process_func(f)

        def decorated(*args, **kwargs):
            value = config.get_property(config_property)
            if not value:
                raise Exception(f"Disabled by config {config_property}")
            return fn(*args, **kwargs)

        return fn_decorator(decorated)
    print(f"inside is_method_enabled, config_properpty is {config_property}")
    return decorator
