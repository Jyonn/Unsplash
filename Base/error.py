class Error:
    NO_LEGAL_USER = 2003
    USER_SAVE_ERROR = 2002
    ERROR_GET_PROFILE = 2001
    ERROR_CODE = 2000
    NEED_LOGIN = 1003
    REQUIRE_JSON = 1002
    REQUIRE_PARAM = 1001
    NOT_FOUND_ERROR = 1000
    OK = 0

    ERROR_DICT = [
        (NO_LEGAL_USER, "无合法用户"),
        (USER_SAVE_ERROR, "保存用户错误"),
        (ERROR_GET_PROFILE, "获取用户信息错误"),
        (ERROR_CODE, "错误的CODE"),
        (NEED_LOGIN, "需要登录"),
        (REQUIRE_JSON, "需要JSON数据"),
        (REQUIRE_PARAM, "缺少参数"),
        (NOT_FOUND_ERROR, "不存在的错误"),
        (OK, "没有错误"),
    ]
