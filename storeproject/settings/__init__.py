from .base import *
from decouple import config

if config("PRODUCTION", default=False, cast=bool):
    from .production import *  # noqa
else:
    from .local import *
