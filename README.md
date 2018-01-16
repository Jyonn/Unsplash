# Unsplash Photo Provider
## 基于Unsplash的高质量图片提供方案

### 获取随机图片
#### REQUEST
```GET https://unsplash.6-79.cn/random```
#### RESPONSE
```
{
    "body": {
        "urls": {
            "small": "https://images.unsplash.com/photo-1474249949617-ca9a962c876a?ixlib=rb-0.3.5&q=80&fm=jpg&crop=entropy&cs=tinysrgb&w=400&fit=max&s=3596162236d483b388b8099990b50617",
            "raw": "https://images.unsplash.com/photo-1474249949617-ca9a962c876a",
            "thumb": "https://images.unsplash.com/photo-1474249949617-ca9a962c876a?ixlib=rb-0.3.5&q=80&fm=jpg&crop=entropy&cs=tinysrgb&w=200&fit=max&s=36ac0e3e66e21ff1e382bd3656c21027",
            "regular": "https://images.unsplash.com/photo-1474249949617-ca9a962c876a?ixlib=rb-0.3.5&q=80&fm=jpg&crop=entropy&cs=tinysrgb&w=1080&fit=max&s=dc6dc476825046b8b8fa2d3177282134",
            "full": "https://images.unsplash.com/photo-1474249949617-ca9a962c876a?ixlib=rb-0.3.5&q=85&fm=jpg&crop=entropy&cs=srgb&s=66009353e8084681d7ee660c2b0c9c2c"
        },
        "color": "#E7C493",
        "width": 5760,
        "height": 3840
    },
    "code": 0,
    "msg": "ok"
}
```

-

### 搜索图片
#### REQUEST
```GET https://unsplash.6-79.cn/search/:keyword```
#### RESPONSE