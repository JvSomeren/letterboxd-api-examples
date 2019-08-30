"""
GET /news
http://api-docs.letterboxd.com/#path--news

Python 3:
$ python3 ./news.py

Python 2.7:
For use with Python 2.7 replace `input(...)` with `raw_input(...)`
$ python ./news.py

"""

import requests
import json
import time
import uuid
import hmac
import hashlib
from getpass import getpass

base_url = 'https://api.letterboxd.com/api/v0'


def search():
    session = requests.Session()
    session.params = {}

    # retrieve your Letterboxd API Key and API Secret
    api_key = input('API Key: ')
    api_secret = getpass('API Secret: ')

    method = 'get'
    url = base_url + '/news'

    # define request headers
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    # define request GET parameters, unique for every request
    params = {
        'apikey': api_key,
        'nonce': uuid.uuid4(),
        'timestamp': int(time.time())
    }
    # available GET parameters are:
    # (see here for the allowed values http://api-docs.letterboxd.com/#/definitions/SearchRequest)
    # params['cursor'] = cursor
    # params['perPage'] = 20

    # prepare the request
    request = requests.Request(method.upper(), url, params=params, headers=headers)
    prepared_request = session.prepare_request(request)

    if prepared_request.body is None:
        encodable_body = ''
    else:
        encodable_body = prepared_request.body

    # create the signature to be sent with the request, recreated for every
    # request as specified here http://api-docs.letterboxd.com/#signing

    # define the salted string
    salted_string = b"\x00".join(
      [str.encode(prepared_request.method), str.encode(prepared_request.url), str.encode(encodable_body)]
    )

    # apply a lower-case HMAC/SHA-256 transformation using your API Secret
    hmac_signature = hmac.new(str.encode(api_secret), salted_string, digestmod=hashlib.sha256)
    signature = hmac_signature.hexdigest()

    # append the signature as the final query parameter
    prepared_request.prepare_url(prepared_request.url, {'signature': signature})
    # as an alternative the following commented line also works
    # prepared_request.headers['Authorization'] = 'Signature ' + signature

    # send the request
    response = session.send(prepared_request)
    json_response = response.json()

    print()

    if response.status_code == 200:
        print(json.dumps(json_response))


if __name__ == "__main__":
    search()
