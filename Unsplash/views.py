from SmartDjango import Analyse
from SmartDjango.p import P
from django.http import HttpResponseRedirect
from django.views import View

from Base.api import UNSPLASH_OAUTH_URI, UnsplashAPI
from Base.rgb import RGB
from Base.similar_photo import SimilarPhoto
from Photo.models import Photo
from User.models import User


class OAuthView(View):
    @staticmethod
    @Analyse.r()
    def get(_):
        return HttpResponseRedirect(UNSPLASH_OAUTH_URI)


class CallbackView(View):
    @staticmethod
    @Analyse.r(q=['code'])
    def get(r):
        code = r.d.code
        access_token = UnsplashAPI.get_access_token(code)
        User.create(access_token)
        return HttpResponseRedirect('/random')


class RandomView(View):
    @staticmethod
    @Analyse.r(q=[P('quick', '快速模式').set_default(0).process(int)], a=[P('size').set_default(None)])
    def get(r):
        quick = r.d.quick
        size = r.d.size
        if size not in ['thumb', 'small', 'regular', 'full', 'raw']:
            size = 'regular'

        if quick:
            return HttpResponseRedirect(Photo.get_random_photo(size))
        return HttpResponseRedirect(User.get_photo()[size])


class InfoView(View):
    @staticmethod
    @Analyse.r(q=[P('quick', '快速模式').set_default(0).process(int)])
    def get(r):
        quick = r.d.quick
        return Photo.get_random_photo() if quick else User.get_photo()


class MultipleView(View):
    @staticmethod
    @Analyse.r(q=[P('num', '数量').set_default(10).process(int)])
    def get(r):
        num = r.d.num
        if num > 50:
            num = 50
        return Photo.get_random_photos(num)


class SearchView(View):
    @staticmethod
    @Analyse.r(a=[P('color', '颜色')])
    def get(r):
        similar_photo = SimilarPhoto(10)
        rgb = RGB(r.d.color)
        for photo in Photo.objects.all():
            c2 = RGB(photo.color)
            dist = RGB.dist(rgb, c2)
            similar_photo.push(dist, photo)
        search_list = [x[1].d() for x in similar_photo.top()]
        return search_list
