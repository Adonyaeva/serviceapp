import requests
# from requests.exceptions.RequestException import ConnectionError
from serviceapp.settings import API_ADDRESS_SERVER_SETTINGS


def send_request(url_type, payload):
    url = API_ADDRESS_SERVER_SETTINGS[url_type]
    # try:
    f = open('text.txt', 'w')
    f.write(str(payload))
    f.close()
    req = requests.get(url, params=payload, auth=(API_ADDRESS_SERVER_SETTINGS['USERS']['USER1']['LOGIN'],
                                     API_ADDRESS_SERVER_SETTINGS['USERS']['USER1']['PASSWORD']))
    result = req.json()
    # except ConnectionError:
    #     result = None
    return result
