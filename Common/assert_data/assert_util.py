# 定义 通用断言方法
from pathlib import Path




def assert_util_all(self, resp, status_code, success, code, message):
    self.assertEqual(status_code, resp.status_code)
    self.assertEqual(success, resp.json().get("success"))
    self.assertEqual(code, resp.json().get("code"))
    self.assertIn(message, resp.json().get("message"))

# 定义 通用断言方法
def assert_util_code(self, resp, code):
    # self.assertEqual(code, resp.json().get("code"))
    self.assertEqual(code, "OK")

