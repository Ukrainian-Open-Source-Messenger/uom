from .handle_login import handle_login
from .handle_register import handle_register


class AuthHandler:
    login = staticmethod(handle_login)
    register = staticmethod(handle_register)
