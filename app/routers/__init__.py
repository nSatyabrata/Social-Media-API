# app/routers/__init__.py
from .auth import *
from .post import *
from .user import *
from .like import *

__all__ = auth.__all__ + post.__all__ +  user.__all__  + like.__all__