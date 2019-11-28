import requests
import json
import base64
import hmac
import hashlib
import logging

from requests.exceptions import RequestException
from django.conf import settings

logger = logging.getLogger('mission')

class HMACAlgorithm(object):
    """
    Performs signing and verification operations using HMAC
    and the specified hash function.
    """
    def __init__(self, hash_alg):
        self.hash_alg = hash_alg
        self.key = None

    def prepare_data(self, data):
        return json.dumps(
            data,
            separators=(',', ':')
        ).encode('utf-8')

    def b64encode(self, byte_string):
        return base64.urlsafe_b64encode(byte_string).replace(b'=', b'')

    def prepare_key(self, key):
        key = key.encode('utf-8')

        invalid_strings = [
            b'-----BEGIN PUBLIC KEY-----',
            b'-----BEGIN CERTIFICATE-----',
            b'-----BEGIN RSA PUBLIC KEY-----',
            b'ssh-rsa'
        ]

        if any([string_value in key for string_value in invalid_strings]):
            raise Exception(
                'The specified key is an asymmetric key or x509 certificate and'
                ' should not be used as an HMAC secret.')
        self.key = key

    def sign(self, msg):
        return hmac.new(self.key, msg, self.hash_alg).digest()


class SprinklrService():
    """Class that handles sprinklr service

    Attributes:
        make_request
        create_user
        create_review
        recipe_reviews
        recipe_ratings
        create_recipe
        update_recipe
    """

    def __init__(self, user_id=None, *args, **kwargs):
        self.user = user_id or settings.SPRINKLR_USER_ID
        self.url = settings.SPRINKLR_HOST
        self.key = settings.SPRINKLR_SECRET_KEY
        self.jwt = settings.SPRINKLR_JWT
        self.site = settings.SPRINKLR_SITE_ID
        logger.info('Init SprinklrService, Host: {}, User: {}, Site: {}'.format(self.url, self.user, self.site))

    def get_token(self, *args, **kwargs):
        logger.info('get_token enter')

        token_payload = {
            "tokenType": "REQUEST",
            "siteId": self.site,
            "aud": ["COMMERCE"],
            "typ": "JWT",
            "authType": "COMMERCE",
            "userId": self.user
        }

        header = {
            "alg": "HS256"
        }

        hmac256 = HMACAlgorithm(hashlib.sha256)
        segments = []

        json_header = hmac256.prepare_data(header)
        json_token = hmac256.prepare_data(token_payload)

        header_byte_str = hmac256.b64encode(json_header)
        token_byte_str = hmac256.b64encode(json_token)

        segments.append(header_byte_str)
        segments.append(token_byte_str)

        signing_input = b'.'.join(segments)
        hmac256.prepare_key(self.key)
        signature = hmac256.sign(signing_input)

        s3 = base64.urlsafe_b64encode(signature).replace(b'=', b'')
        segments.append(s3)

        return b'.'.join(segments).decode('utf-8')

    def make_request(self, endpoint, payload, method):
        """Makes a request to sprinklr service"""
        try:
            token = self.get_token()
            headers = {
                "Authorization": "Bearer {0}".format(token)
            }
            logger.info('SprinklrService:make_request, Endpoint: {}, Payload: {}, Token: {}'.format(endpoint, payload, token))
            r = requests.request(
                method,
                "{0}{1}".format(self.url, endpoint),
                headers=headers,
                data=payload
            )
            resp = r.json()
        except RequestException as e:
            resp = json.dumps({
                "message": str(e)
            })
        logger.info('SprinklrService:make_request, Response: {}'.format(resp))
        return resp

    def create_user(self, payload={}, *args, **kwargs):
        """Creates a user into the sprinklr service
            It receives a dict with the payload to be sent i.e.
            payload = {
                "id": "bocud-2",
                "firstName": "Testing",
                "displayName": "test001",
                "admin": False,
                "verified": True,
                "trusted": True,
                "anonymous": False,
                "email": "testing@mail.com"
            }
        """

        endpoint = "/users"
        method = "POST"
        return self.make_request(endpoint, json.dumps(payload), method)

    def get_user(self, user_id=None, *args, **kwargs):
        """Get a user from the sprinklr service
            It receives a dict with the payload to be sent i.e.
            payload = {}
        """

        endpoint = "/users/{0}".format(user_id)
        method = "GET"
        return self.make_request(endpoint, {}, method)

    def create_review(self, payload={}, *args, **kwargs):
        """Creates a review into the sprinklr service
            It receives a dict with the payload to be sent i.e.
            payload = {
                "rating": {
                    "value": 5
                },
                "title": "Great Tortilla",
                "body": "I have a positive opinion of this product",
                "isBodyHTML": False,
                "productId": "product-001"
            }
        """

        endpoint = "/reviews"
        method = "POST"
        return self.make_request(endpoint, json.dumps(payload), method)

    def recipe_reviews(self, recipe_id=None, *args, **kwargs):
        """Fetches a recipe reviews from the sprinklr service
            It receives the id of the product
        """

        endpoint = "/products/{0}/reviews".format(recipe_id)
        method = "GET"
        response = self.make_request(endpoint, {}, method)
        try:
            return response.get('list', [])
        except AttributeError:
            return []


    def recipe_ratings(self, recipe_id=None, *args, **kwargs):
        """Fetches a recipe average rating from the sprinklr service
            It receives the id of the product
        """

        endpoint = "/products/{0}".format(recipe_id)
        method = "GET"
        resp = self.make_request(endpoint, {}, method)
        average_rating = resp.get("product", {}).get("averageRating", 0)
        logger.info('SprinklrService - recipe_ratings, average_rating: {}'.format(average_rating))
        return average_rating

    def create_recipe(self, payload={}, *args, **kwargs):
        """Creates a product into the sprinklr service
            It receives a dict with the payload to be sent i.e.
            payload = {
                "id": "product-001",
                "name": "Product 001",
                "description: "description 001"
            }
        """
        endpoint = "/products"
        method = "POST"
        return self.make_request(endpoint, json.dumps(payload), method)

    def update_recipe(self, recipe_id=None, payload={}, *args, **kwargs):
        """Updates a product into the sprinklr service
            It receives a dict with the payload to be sent i.e.
            payload = {
                "id": "product-001",
                "name": "Product 001",
                "description: "description 001"
            }
        """
        endpoint = "/products/{0}".format(recipe_id)
        method = "PUT"
        return self.make_request(endpoint, json.dumps(payload), method)
