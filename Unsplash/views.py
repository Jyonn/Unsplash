from django.http import HttpResponseRedirect
from django.views import View
from smartdjango import analyse, Validator

from Base.api import UNSPLASH_OAUTH_URI, UnsplashAPI
from Base.rgb import RGB
from Base.similar_photo import SimilarPhoto
from Photo.models import Photo
from User.models import User


class OAuthView(View):
    def get(self, request):
        return HttpResponseRedirect(UNSPLASH_OAUTH_URI)


class CallbackView(View):
    @analyse.query('code')
    def get(self, request):
        code = request.d.code
        access_token = UnsplashAPI.get_access_token(code)
        User.create(access_token)
        return HttpResponseRedirect('/random')


class RandomView(View):
    @analyse.query(Validator('quick', '快速模式').default(0).to(int).null())
    @analyse.argument(Validator('size').default(None).null())
    def get(self, request, **kwargs):
        quick = request.query.quick
        size = request.argument.size
        if size not in ['thumb', 'small', 'regular', 'full', 'raw']:
            size = 'regular'

        if quick:
            return HttpResponseRedirect(Photo.get_random_photo(size))
        return HttpResponseRedirect(User.get_photo()[size])


class InfoView(View):
    @analyse.query(Validator('quick', '快速模式').default(0).to(int).null())
    def get(self, request):
        quick = request.query.quick
        return Photo.get_random_photo() if quick else User.get_photo()


class MultipleView(View):
    @analyse.query(Validator('num', '数量').default(10).to(int).null())
    def get(self, request):
        num = request.query.num
        if num > 50:
            num = 50
        return Photo.get_random_photos(num)


class SearchView(View):
    @analyse.argument(Validator('color', '颜色'))
    def get(self, request, **kwargs):
        similar_photo = SimilarPhoto(10)
        rgb = RGB(request.argument.color)
        for photo in Photo.objects.all():
            c2 = RGB(photo.color)
            dist = RGB.dist(rgb, c2)
            similar_photo.push(dist, photo)
        search_list = [x[1].d() for x in similar_photo.top()]
        return search_list


class CountView(View):
    def get(self, request):
        return Photo.objects.count()
