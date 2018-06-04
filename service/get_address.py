import requests
from django.conf import settings
# from requests.exceptions.RequestException import ConnectionError
from serviceapp.settings import API_ADDRESS_SERVER_SETTINGS
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

@cache_page(CACHE_TTL)
def send_request(url_type, payload):
    url = API_ADDRESS_SERVER_SETTINGS[url_type]
    req = requests.get(url, params=payload, auth=(API_ADDRESS_SERVER_SETTINGS['USERS']['USER1']['LOGIN'],
                                     API_ADDRESS_SERVER_SETTINGS['USERS']['USER1']['PASSWORD']))
    result = req.json()
    return result
