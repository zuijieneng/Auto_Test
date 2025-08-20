import unittest
from tokenize import cookie_re

import requests


class GdcDevicesApi(object):
    @classmethod
    def get_device_pages(cls, token):
        url='https://gdc.cern.ch/api/v2/login'
        header = {"Content-Type": "application/json",
                  "Authorization": f"Bearer {token}"}
        response = requests.request("POST", url, headers=header)
        return response.json()
