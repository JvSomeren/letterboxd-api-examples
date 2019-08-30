"""
GET/PATCH /me
http://api-docs.letterboxd.com/#path--me

Python 3:
$ python3 ./me.py

Python 2.7:
For use with Python 2.7 replace `input(...)` with `raw_input(...)`
$ python ./me.py

To update the profile add the `--patch` argument when running the program

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


def me_get():
    session = requests.Session()
    session.params = {}

    # retrieve your Letterboxd API Key and API Secret
    api_key = input('API Key: ')
    api_secret = getpass('API Secret: ')

    method = 'get'
    url = base_url + '/me'

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
    json_response = response.json()

    print()

    if response.status_code == 200:
        print(json.dumps(json_response))
    elif response.status_code == 401:
        print('There is no authenticated member')


def me_patch():
    session = requests.Session()
    session.params = {}

    # retrieve your Letterboxd API Key and API Secret
    api_key = input('API Key: ')
    api_secret = getpass('API Secret: ')

    method = 'patch'
    url = base_url + '/me'

    # define request headers as specified here http://api-docs.letterboxd.com/#auth
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    access_token = input('Access token: ')
    headers['Authorization'] = 'Bearer ' + access_token

    # define request body
    # available POST body properties are:
    # (see here for the allowed values http://api-docs.letterboxd.com/#/definitions/MemberSettingsUpdateRequest)
    body = {}
    # body['emailAddress'] = 'me@example.com'
    # body['currentPassword'] = 'hunter2'
    # body['password'] = 'hunter3'
    # body['givenName'] = 'Tony'
    # body['familyName'] = 'Stark'
    # body['pronoun'] = '3R'  # He / his; use GET `/members/pronouns` for a full list of pronouns
    # body['location'] = 'New York'
    # body['website'] = 'https://example.com'
    # body['bio'] = 'I am Iron Man.'
    # body['favoriteFilms'] = ['28dA', '2cBQ']  # Iron Man and Iron Man 3 respectively
    # body['privateAccount'] = False
    # body['includeInPeopleSection'] = True
    # body['emailWhenFollowed'] = True
    # body['emailComments'] = True
    # body['emailNews'] = True
    # body['emailRushes'] = True
    body = json.dumps(body)

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

    print(response)

    print()

    if response.status_code == 200:
        print(json.dumps(json_response))
    elif response.status_code == 400:
        print('Bad request')
    elif response.status_code == 401:
        print('There is no authenticated member')


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('--patch', action='store_true', dest='patch',
                        help='Update the profile.')

    args = parser.parse_args()

    if args.patch is True:
        me_patch()
    else:
        me_get()
