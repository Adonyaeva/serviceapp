from django.conf import settings
import os
from urllib.request import urlopen, URLError
import json
import requests

def send_request():
    url = API_ADDRESS_SERVER_SETTINGS['URL_FLAT'] + '?house=' + request.GET['house_id']
    try:
        result = requests.get(url, auth=(API_ADDRESS_SERVER_SETTINGS['USERS']['USER1']['LOGIN'],
                                         API_ADDRESS_SERVER_SETTINGS['USERS']['USER1']['PASSWORD']))
        flats = json.loads(result.content)
    except URLError as e:
        return e
