import logging
import unittest

from api.dubbo_service.device_service import DeviceService
from api.gdc_devices_api import GdcDevicesApi
from Configs.logger_config import init_log_config
from Common.requests_util.token_util import get_header_by_user
from Configs import BASE_LOG_DIR


class TestDeviceService(unittest.TestCase):
    service = None
    header = None

    @classmethod
    def setUp(cls):
        # 封装头部：有token
        cls.header = get_header_by_user()

    @classmethod
    def setUpClass(cls):
        cls.service = DeviceService()
        init_log_config(BASE_LOG_DIR + 'test_device.log')

    @classmethod
    def device_is_exist(self):
        resp = self.service.get_device_by_device_code("gdc_device_voc")
        logging.info(resp)
        self.assertEqual(resp.get("device_code"), "gdc_device_voc")

    @classmethod
    def device_is_not_exist(self):
        resp = self.service.get_device_by_device_code("gdc_device_voc")
        self.assertEqual(None, resp)

    @classmethod
    def add_device_code_is_repeat(self):
        device = {"deivce_code": "gdc_device_voc", "device_name": "gdc设备"}
        resp = self.service.add_device(device)
        # 记住调用service方法结果返回肯定是json序列化对象，不是接口的code、msg等等，注意别搞混了，底层不一样，requests走接口，这里直接调用方法
        self.assertEqual(None, resp)  # 设备code已存在

    @classmethod
    def get_device_list(slef, token):
        devices_page = GdcDevicesApi.get_device_pages(token)



