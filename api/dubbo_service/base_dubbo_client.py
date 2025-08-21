from dubboclient import DubboClient

from Common.handle_data.config_parse import ConfigParse


class BaseDubboClient(object):
    dubboclient = None
    service_name = None

    def __init__(self):
        config = ConfigParse()
        host = config.get_value("host", "host")
        port = config.get_value("host", "port")
        self.dubboclient = DubboClient(host, port)
