"""
POST /me/validation-request
http://api-docs.letterboxd.com/#path--me-validation-request

Python 3:
$ python3 ./me_validation-request.py

Python 2.7:
For use with Python 2.7 replace `input(...)` with `raw_input(...)`
$ python ./me_validation-request.py

"""

import requests
import json
import time
import uuid
import hmac
import hashlib
from getpass import getpass
from argparse import ArgumentParser

base_url = 'https://api.letterboxd.com/api/v0'


def me_validation_request():
    session = requests.Session()
    session.params = {}

    # retrieve your Letterboxd API Key and API Secret
    api_key = input('API Key: ')
    api_secret = getpass('API Secret: ')

    method = 'post'
    url = base_url + '/me/validation-request'

    # define request headers as specified here http://api-docs.letterboxd.com/#auth
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    access_token = input('Access token: ')
    headers['Authorization'] = 'Bearer ' + access_token

    # define request GET parameters, unique for every request
    params = {
        'apikey': api_key,
        'nonce': uuid.uuid4(),
        'timestamp': int(time.time())
    }

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

    print()

    if response.status_code == 204:
        print('Success (the email was dispatched if it matched an existing account)')
    elif response.status_code == 401:
        print('There is no authenticated member')
    elif response.status_code == 403:
        print('The authenticated member\'s email address was already successfully validated.')
    elif response.status_code == 429:
        print('Too many validation requests have been requested. The email is probably in the member\'s spam folder.')


if __name__ == "__main__":
    me_validation_request()
