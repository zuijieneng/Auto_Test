from dubboclient import DubboClient

from api.dubbo_service.base_dubbo_client import BaseDubboClient

'''
DubboClient是重要的分布式测试工具体，通过DubboClient调用本地或远程服务，验证业务逻辑。
比如获取设备，需要获取当前用户的角色权限，就需要远程调用另一个模块里的服务，这时候无法直接在游览器或手机抓包，那么就用这个工具进行远程调用。
可以做到对角色权限接口的单元测试，并且不用同时启用设备服务和角色服务。
'''


# DeviceService是BaseDubboClient的子类
class DeviceService(BaseDubboClient):

    # 创建类对象的时候调用，类似Java默认的构造方法
    def __init__(self):
        super().__init__()
        self.service = "DeviceService"  # 赋值

    # 添加参数
    def get_device_by_device_code(self, device_code):
        return self.dubboclient.invoke(self.service_name, "getDeviceByDeviceId", device_code)

    # 添加对象
    def add_device(self, device):
        device["class"] = "com.gdc.pg.pojo.Device"
        return self.dubboclient.invoke(self.service_name, "addDevice", device)


if __name__ == '__main__':
    deviceService = DeviceService()
    device = {"id": "12124189u", "device_name": "shhshsi", "date": "2019-11-19 11:11:02"}
    resp = deviceService.add_device(device)
    resp2 = deviceService.get_device_by_device_code("codecode")
