from .handle_login import handle_login
from .handle_register import handle_register
from .handle_verify_token import handle_verify_token

class AuthHandler:
    login = staticmethod(handle_login)
    register = staticmethod(handle_register)
    verify_token = staticmethod(handle_verify_token)
