"""
POST /auth/token
http://api-docs.letterboxd.com/#path--auth-token

Python 3:
$ python3 ./auth_token.py

Python 2.7:
For use with Python 2.7 replace `input(...)` with `raw_input(...)`
$ python ./auth_token.py

To refresh a token add the `--refresh` argument when running the program

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


def auth_token_generate():
    session = requests.Session()
    session.params = {}

    # retrieve your Letterboxd API Key and API Secret
    api_key = input('API Key: ')
    api_secret = getpass('API Secret: ')

    method = 'post'
    url = base_url + '/auth/token'

    # define request headers as specified here http://api-docs.letterboxd.com/#auth
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }

    username = input('Username or email address: ')
    password = getpass('Password: ')

    # define request body as specified here http://api-docs.letterboxd.com/#auth
    body = {
        'grant_type': 'password',
        'username': username,
        'password': password
    }

    # define request GET parameters, unique for every request
    params = {
        'apikey': api_key,
        'nonce': uuid.uuid4(),
        'timestamp': int(time.time())
    }

    # prepare the request
    request = requests.Request(method.upper(), url, data=body, params=params, headers=headers)
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

    # on failed authentication
    if response.status_code == 400:
        print('The credentials were not correct for the member, or the account was not found.')
        print('Response:')
        print(json.dumps(json_response, indent=4))
        return

    # on successful authentication
    print('Response:')
    print(json.dumps(json_response, indent=4))


def auth_token_refresh():
    session = requests.Session()
    session.params = {}

    # retrieve your Letterboxd API Key and API Secret
    api_key = input('API Key: ')
    api_secret = getpass('API Secret: ')

    method = 'post'
    url = base_url + '/auth/token'

    # define request headers as specified here http://api-docs.letterboxd.com/#auth
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }

    refresh_token = input('Refresh token: ')

    # define request body as specified here http://api-docs.letterboxd.com/#auth
    body = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    }

    # define request GET parameters, unique for every request
    params = {
        'apikey': api_key,
        'nonce': uuid.uuid4(),
        'timestamp': int(time.time())
    }

    # prepare the request
    request = requests.Request(method.upper(), url, data=body, params=params, headers=headers)
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

    # on failed authentication
    if response.status_code == 400:
        print('The credentials were not correct for the member, or the account was not found.')
        print('Response:')
        print(json.dumps(json_response, indent=4))
        return

    # on successful authentication
    print('Response:')
    print(json.dumps(json_response, indent=4))


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('--refresh', action='store_true', dest='refresh',
                        help='Refresh a token.')

    args = parser.parse_args()

    if args.refresh is True:
        auth_token_refresh()
    else:
        auth_token_generate()
