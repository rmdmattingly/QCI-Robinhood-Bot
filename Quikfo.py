import json
import acct
import requests

def getQCIs():
    endpoint = 'https://quikfo.com/api/v1/qci/all/'
    key = '?key=' + acct.key
    return json.loads(requests.get(endpoint + key).text)