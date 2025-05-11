from decouple import config

from .base import *

if config("PRODUCTION", default=False, cast=bool):
    from .production import *  # noqa
else:
    from .local import *
