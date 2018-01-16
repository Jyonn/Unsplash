""" 171203 Adel Liu

弃用session，该用jwt
"""

# from User.models import User
# from Base.error import Error
# from Base.response import Ret
# from Base.session import load_session, save_session


DEBUG = True


def deprint(*args):
    """
    系统处于调试状态时输出数据
    """
    if DEBUG:
        print(*args)


# def get_user_from_session(request):
#     user_id = load_session(request, 'user', once_delete=False)
#     if user_id is None:
#         return Ret(Error.REQUIRE_LOGIN)
#     return User.get_user_by_id(user_id)
#
#
# def save_user_to_session(request, user):
#     try:
#         request.session.cycle_key()
#     except:
#         pass
#     save_session(request, 'user', user.pk)
#     return None
#
#
# def logout_user_from_session(request):
#     load_session(request, 'user')
