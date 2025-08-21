import configparser
import logging

from Configs.file_path_config import get_file_path
from Configs.logger_config import init_log_config


class ConfigParse:
    def __init__(self, file_name="config.ini"):
        # 日志打印
        init_log_config("config_parse.log")
        # 该类的属性：配置文件名称
        self.file_name = file_name
        # 该类的属性：文件路径
        self.file_path = get_file_path(file_name)
        # 配置解析器
        self.config = configparser.ConfigParser()
        # 文件存在则读取
        if self.file_path is not None:
            self.config.read(self.file_path, encoding="utf-8")  # 解析器读取文件

    def get_value(self, head_arg, next_arg):
        if self.file_path is None:
            logging.error(f"配置文件:{self.file_name}的地址不存在，详情请看file_path_config.py是否配置了相关地址")
        return self.config.get(head_arg, next_arg)

    def get_base_url(self, node_name):
        return self.get_value(node_name, 'base_url')

    def get_mysql_config(self, node_name):
        return self.get_value('mysql', node_name)

    @classmethod
    def get_headers(self, node_name):
        return self.get_value('headers', node_name)

# if __name__ == '__main__':
#     config = ConfigParse("文件.kl")
#     Result = config.get_value("host", "host")
#     print(Result)
