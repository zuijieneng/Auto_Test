from dubboclient import DubboClient


class BaseDubboClient(object):
    dubboclient = None
    service_name = "DeviceService"

    def __init__(self):
        self.dubboclient = DubboClient("192.168.127.12", 8080)



