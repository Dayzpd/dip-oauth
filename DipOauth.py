from urllib.parse import urlencode
import requests
import random
import string
import json

REQUIRED_AUTH_KEYS = [
    'client_id',
    'redirect_uri',
    'response_type',
    'scope'
]

REQUIRED_TOKEN_KEYS = [
    'code',
    'client_id',
    'client_secret',
    'redirect_uri',
    'grant_type'
]

REQUIRED_REFRESH_KEYS = [
    'client_id',
    'client_secret',
    'refresh_token',
    'grant_type'
]


class DipOauth(object):
    def __init__(self, auth_uri, token_uri):
        '''
        Initalize DipOuth object.
        Args:
            - auth_uri (REQUIRED): Authorization endpoint for the API you want
                                   to access.
            - token_uri (REQUIRED): Token endpoint for the API used to fetch and
                                    refresh tokens.
        Raises:
            - ValueError: You must provide an auth_uri and token_uri.
        '''
        if auth_uri == None or token_uri == None:
            raise ValueError(
                'The DipOauth class requires that you specify the authorization' +
                'endpoint uri and token endpoint uri.'
            )
        self.auth_uri = auth_uri
        self.token_uri = token_uri

    def get_auth_code_link(self, **kwargs):
        '''
        Retrieve the authorization code.
        Args:
            - client_id (REQUIRED): Client ID for the API you want to access.
            - redirect_uri (REQUIRED): Your application redirect uri.
            - response_type (REQUIRED): Response type you want from the API
                                        (e.g. 'code')
            - scope (REQUIRED): The API resources you would like to access.
        Raises:
            - ValueError: If you don't provide the required keys, a ValueError
                          will be raised.
            - requests.exceptions.HTTPError: Request failed with status other
                                             than 200. Check error message for
                                             more details.
        Returns:
            - auth_url: URL to initiate Oauth flow.
            - state: State to confirm that the callback is valid.
        '''
        global REQUIRED_AUTH_KEYS
        self.verify_args(REQUIRED_AUTH_KEYS, kwargs)
        state = self.generate_state()
        auth_url = self.auth_uri + '?' + urlencode(kwargs) + '&state=' + state
        return auth_url, state

    def fetch_token(self, **kwargs):
        '''
        Fetch the token from the API in order to access user data.
        Args:
            - code (REQUIRED): The code that you received in the arguments from
                               the callback.
            - client_id (REQUIRED): Client ID for the API you want to access.
            - client_secret (REQUIRED): Client secret for the API you want to
                                        access.
            - redirect_uri (REQUIRED): Your application redirect uri.
            - grant_type (REQUIRED): The grant type for the API access (e.g.
                                     'authorization_code').
        Raises:
            - ValueError: If you don't provide the required keys, a ValueError
                          will be raised.
            - requests.exceptions.HTTPError: Request failed with status other
                                             than 200. Check error message for
                                             more details.
        Returns:
            - access_token: API access token.
            - expires_in: Number of seconds until the access token expires.
            - token_type: Type of token.
            - refresh_token: Refresh token used to get new access token when it
                             expires.
        '''
        global REQUIRED_TOKEN_KEYS
        self.verify_args(REQUIRED_TOKEN_KEYS, kwargs)
        token_url = self.token_uri
        res = requests.post(
            token_url,
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            data=kwargs
        )
        if res.status_code != 200:
            res.raise_for_status()

        return json.loads(res.text)

    def refresh_token(self, **kwargs):
        '''
        Refresh your access token.
        Args:
            - refresh_token (REQUIRED): The refresh token that you received
                                        when fetching the original token.
            - client_id (REQUIRED): Client ID for the API you want to access.
            - client_secret (REQUIRED): Client secret for the API you want to
                                        access.
            - grant_type (REQUIRED): The grant type for the API access (e.g.
                                     'authorization_code').
        Raises:
            - ValueError: If you don't provide the required keys, a ValueError
                          will be raised.
            - requests.exceptions.HTTPError: Request failed with status other
                                             than 200. Check error message for
                                             more details.
        Returns:
            - access_token: API access token.
            - expires_in: Number of seconds until the access token expires.
            - token_type: Type of token.
        '''
        global REQUIRED_REFRESH_KEYS
        self.verify_args(REQUIRED_REFRESH_KEYS, kwargs)
        token_url = self.token_uri
        res = requests.post(
            token_url,
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            data=kwargs
        )
        if res.status_code != 200:
            res.raise_for_status()
        return json.loads(res.text)

    def generate_state(self):
        chars = string.ascii_lowercase + string.digits
        return ''.join(random.choice(chars) for _ in range(30))

    def verify_args(self, required_keys, provided_keys):
        if not all(key in provided_keys for key in required_keys):
            raise ValueError(
                'Keys provided include [' + ', '.join(provided_keys) +
                '], but this method requires [' + ', '.join(required_keys) + ']'
            )
