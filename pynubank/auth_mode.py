from enum import Enum
from functools import wraps

from pynubank.exception import NuInvalidAuthenticationMethod


class AuthMode(Enum):
    UNAUTHENTICATED = 0
    WEB = 1
    APP = 2


def requires_auth_mode(*required_auth_mode: AuthMode):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            instance = args[0]
            if instance._auth_mode not in required_auth_mode:
                raise NuInvalidAuthenticationMethod(
                    'The authentication method used doest not allow access to this resource'
                )

            return function(*args, **kwargs)

        return wrapper

    return decorator
