from smartdjango import Error, Code


@Error.register
class UserErrors:
    CREATE = Error("创建用户失败", code=Code.InternalServerError)
    NO_LEGAL_USER = Error("没有合法用户", code=Code.ServiceUnavailable)


class UserValidator:
    MAX_USER_ID_LENGTH = 20
    MAX_USERNAME_LENGTH = 20
    MAX_ACCESS_TOKEN_LENGTH = 64
