from smartdjango import Error, Code


@Error.register
class PhotoErrors:
    CREATE = Error('创建图片失败', code=Code.InternalServerError)
    EXISTS = Error('图片已存在', code=Code.BadRequest)


class PhotoValidator:
    MAX_PHOTO_ID_LENGTH = 20
    MAX_COLOR_LENGTH = 10
