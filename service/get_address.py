import requests
import logging
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page

from requests.exceptions import ConnectionError
from serviceapp.settings import API_ADDRESS_SERVER_SETTINGS

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


@cache_page(CACHE_TTL)
def send_request(url_type, payload):
    url = API_ADDRESS_SERVER_SETTINGS[url_type]
    try:
        req = requests.get(url, params=payload, auth=(API_ADDRESS_SERVER_SETTINGS['USERS']['USER1']['LOGIN'],
                                         API_ADDRESS_SERVER_SETTINGS['USERS']['USER1']['PASSWORD']))
        result = req.json()
        return result
    except ConnectionError as e:
        logging.warning(e)
