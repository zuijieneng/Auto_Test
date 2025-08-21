import unittest

import pytest
import requests
from ddt import ddt, file_data
from Common.assert_data.assert_util import assert_util_code
from Configs.logger_config import init_log_config
from Configs import BASE_LOG_DIR, BASE_FILE_DIR


@ddt
class TestLogin(unittest.TestCase):
    def setUp(self):
        init_log_config(BASE_LOG_DIR + "test.log")

    # 登陆模块
    # @parameterized.expand(get_json_to_list_data("login_data.json"))
    # @pytest.mark.flaky(reruns=3, reruns_delay=3)  # 重跑设置（次数=3），时间间隔2s
    @file_data(BASE_FILE_DIR.joinpath("login_data.json"))
    def test_login(self, **user):  # **在python中是解析关键参数的意思，如果是*是接收位置参数
        url = "http://xxxx:8888/api/admin/code/login"  # 登陆的URL地址
        json_data = {"username": user["username"],
                     "password": user["password"]}  # json_data = f"username:{username}, password: {pwd} "
        header = {"Content-Type": "application/json"}
        resp = requests.post(url=url, headers=header, json=json_data)
        assert_util_code(self, resp, user["code"])
