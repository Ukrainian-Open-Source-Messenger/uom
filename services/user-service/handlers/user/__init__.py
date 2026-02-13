from .handle_make_user import handle_make_user
from .handle_get_me_by_email import handle_get_me_by_email
from .handle_get_me_by_id import handle_get_me_by_id

class UserHandler:
    make_user = staticmethod(handle_make_user)
    get_me_by_email = staticmethod(handle_get_me_by_email)
    get_me_by_id = staticmethod(handle_get_me_by_id)
