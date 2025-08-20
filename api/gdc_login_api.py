import unittest
from tokenize import cookie_re

import requests


class GdcLoginApiTest(object):
    @classmethod
    def login_api(cls, json_data):

