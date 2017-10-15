from urllib.parse import urlencode

import requests

from Base.common import deprint
from Base.decorator import logging
from Settings.models import Settings

client_id = Settings.objects.get('unsplash-client-id')
secret = Settings.objects.get('unsplash-secret')
redirect_uri = Settings.objects.get('unsplash-redirect-uri')

host = 'https://api.unsplash.com'
authorize_url = host + '/oauth/authorize'
token_url = host + '/oauth/token'
user_profile_url = host + '/me'


@logging
def oauth_link():
    return '%s?client_id=%s&redirect_uri=%s&response_type=code&scope=public+read_user' \
           % (authorize_url, client_id, redirect_uri)


@logging
def get_access_token(token):
    params = {
        'client_id': client_id,
        'client_secret': secret,
        'redirect_uri': redirect_uri,
        'code': token,
        'grant_type': 'authorization_code',
    }

    try:
        response = requests.post(token_url, json=params)
        if response.status_code == 200:
            deprint('CONTENT -- ', response.content)
            return response.json()
    except:
        return None


@logging
def get_user_profile(access_token):
    params = {
        'access_token': access_token,
    }
    params_encoded = urlencode(params)
    headers = {'content-type': 'application/json'}

    try:
        response = requests.get(user_profile_url, params=params_encoded, headers=headers)
        if response.status_code == 200:
            deprint('CONTENT -- ', response.content)
            return response.json()
    except:
        return None
