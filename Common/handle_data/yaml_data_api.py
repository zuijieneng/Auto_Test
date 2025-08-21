import logging
from pathlib import Path
from typing import Optional, Any
import yaml
from pywin.mfc.object import Object

from Common.handle_data.config_parse import ConfigParse
from Configs.file_path_config import get_file_path
from Configs.logger_config import init_log_config


class YamlDataApi(Object):

    def __init__(self, file_name="test.yaml", path=get_file_path("datas")):
        self.file_path = path
        self.file_name = file_name
        if file_name is not None:
            self.file_path = self.file_path / file_name
        init_log_config("handle_yaml_data.log")

    def read_yaml_data(self, node_str=None, separator=".", list_type=0) -> Optional[Any]:
        '''
        递归读取yaml数据（原理：类似于二叉树的遍历）
        :param node_str: 所有节点的信息，按照顺序一次组装，默认用逗号隔开
        :param separator: node_str的分割符号，默认是逗号
        :param list_type: 所有节点数据是列表，那么返回的结果是：0代表列表（默认），1代表字符串（默认用逗号隔开）
        :return: -> Optional[Any]返回结果可以是多种任意类型
        '''
        try:
            # 1. 解析整个YAML文件
            with open(self.file_path, 'r', encoding='utf-8') as f:
                yaml_data = yaml.safe_load(f)
                if yaml_data is None:
                    logging.error(f"解析度文件{self.file_name}内容为空！")
                    return None
            # 2. 节点信息分割
            if node_str is None: return yaml_data
            node_list = node_str.split(separator)
            # 3. 递归读取yaml数据
            def recursive_read(current_data, remaining_nodes: list[str]) -> Optional[Any]:
                # 递归终止条件：所有节点都已经遍历过了（列表为空）
                if not remaining_nodes:
                    # TODO 这里可以判断数据类型，如果是列表，可以返回列表，也可以返回字符串，根据需求定
                    return current_data
                # 获取节点
                current_node = remaining_nodes[0]

                # [1]处理列表类型（支持通过索引访问，如"list.0"）
                if isinstance(current_data, list):
                    try:
                        return recursive_read(current_data[int(current_node)], remaining_nodes[1:])  # 用切片方法截取
                    except ValueError:
                        logging.error(f"数据是列表类型，因此获取数据只能用下标获取！,但{current_node}非数字类型！")
                        return None
                # [2]处理字典类型
                elif isinstance(current_data, dict):
                    if current_node in current_data:
                        return recursive_read(current_data[current_node], remaining_nodes[1:])
                    else:
                        logging.error(f"数据是字典类型，但是节点{current_node}不存在！")
                        return None
                # [3]非容器类型（无法继续解析子节点）
                else:
                    logging.error(f"节点 {current_node} 不是字典或列表，无法继续解析")
                    return None

            # 4.启动递归查询
            return recursive_read(yaml_data, node_list)
        except Exception as e:
            logging.error(e)

    def write_all_datas(self, data):
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                if f is None:
                    Path.mkdir(self.file_path)
                # 如果是字典类型数据，那么写入文件
                if isinstance(data, dict):
                    yaml.dump(data=data, stream=f, allow_unicode=True, sort_keys=False)
                else:
                    logging.error(f"类Handle_Yaml的write_data方法处理文件失误：数据格式不正确！不是字典类型！")
        except Exception as e:
            logging.error(f"类Handle_Yaml的write_data方法处理文件失误:{e}")

    def clear_all_datas(self):
        try:
            with open(self.file_name, encoding="utf-8", mode='w') as f:
                f.truncate()
        except Exception as e:
            logging.error(f'类Handle_Yaml的clear_data方法处理文件失误: {e}')


if __name__ == '__main__':
    handle = YamlDataApi("test.yaml").read_yaml_data("testCase.data.device_users")
    print(handle)
