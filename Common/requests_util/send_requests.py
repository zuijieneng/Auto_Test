import ast
import logging
import re
import requests
from Configs.logger_config import init_log_config


class SendRequests:
    def __init__(self):
        init_log_config('send_requests.log')

    @classmethod
    def decode_response_text(cls, response_text):
        """
        如果返回的结果里面有中文需要解码
        :param response_text: 包含可能 Unicode 转义字符的响应文本
        :return: 理后的文本，已解码 Unicode 转义字符
        """
        if re.search(r"\\u[0-9a-fA-F]{4}", response_text):
            return response_text.encode().decode('unicode_escape')  # encode将str转换成byte
        return response_text

    def send_request(self, **kwargs):
        # 创建一个会话
        session = requests.Session()
        try:
            response = session.request(**kwargs)
            # 保存账号的cookie
            requests.utils.cookiejar_from_dict(response.cookies, overwrite=True)
            # 写入到相应的文件保存

        except requests.exceptions.ConnectionError as e:
            logging.error('接口请求异常,可能是request的链接过多或者速度过快导致程序报错! ')
        except requests.exceptions.RequestException as e:
            logging.error("请求异常,请检查系统数据是否正常!")
        return response

    def execute_api_request(self, url, method, headers, cookies=None, file=None, api_name=None, case_name=None,
                            **kwagrs):
        ''' 发起接口请求
        :param api_name: 接口名称（打印日志用的）
        :param url: 接口地址
        :param method: 请求方法
        :param headers: 请求头
        :param case_name: 用例名称（打印日志用的）
        :param cookie: cookie（默认为None，非必填）
        :param file: file（默认为None，非必填）
        :return:
        '''
        return self.send_request(
            url=url,
            method=method,
            headers=headers,
            cookies=cookies,
            files=file,
            timeout=10,
            verify=True,
            **kwagrs)






# if __name__ == '__main__':
#     url = "http://baidu.com"
#     method = 'get'
#     headers = {
#         "Content-Type": "application/json; charset=utf-8"
#     }
#     cookies = {
#         'cookies': 'MYJ_wig5buyoga=JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjJhZDJhMDYxNC0xZDczLTRlNzMtYTc1Yy1hZTlmOGU0ZmU3YjMlMjIlMkMlMjJ1c2VySWQlMjIlM0ElMjIxNDMwJTIyJTJDJTIycGFyZW50SWQlMjIlM0ElMjIxMjIlMjIlMkMlMjJzZXNzaW9uSWQlMjIlM0ExNzQ3MTkxNzI5NTY0JTJDJTIyb3B0T3V0JTIyJTNBZmFsc2UlMkMlMjJsYXN0RXZlbnRUaW1lJTIyJTNBMTc0NzE5MjI5MTQwMiUyQyUyMmxhc3RFdmVudElkJTIyJTNBMzIlN0Q=; MYJ_MKTG_wig5buyoga=JTdCJTdE; oms_u=0O7VU868%2BGN9idGLWGUaC%2BJe5C0mVYSKQYaHuW9uWK3vL4CKOiqYyjlx37hvpkePrWwcb%2FjAihWIiShvGuIMswGN%2Blpy4BqDkvrtLWhqsq3Nuk2SedbzV4OpLv68xqpYeHEISBTcq9slyPJVJ7t37YVtzAOenQaDFXUUkMxufQftdJCwKl0QjX%2Fg7LtWNl7%2BZawpnyUPY889r68xwG9gBIJCNEiTYAS3PZyIYkTqIrWPT1EpVNpmSh0%2F8kdKPCr2XkE1qn0sI%2F8x0VcIo14n4IxeGyD2t%2Bh3Uns4J9OzgaQd0HZPQi8wmLxWKDM9WaGGhaW9AGotNy1F4MXIj%2FjGWB4xD1pgG7OHFuIXhzIaXiY%3D; MYJ_MKTG_u2j1jks593=JTdCJTdE; MYJ_u2j1jks593=JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjJiNDkyOTUyZC1lODk3LTQxZmYtYjEyNy0wNTM5OWU5ZTAxNmYlMjIlMkMlMjJ1c2VySWQlMjIlM0ElMjIxMjIlMjIlMkMlMjJwYXJlbnRJZCUyMiUzQSUyMjEyMiUyMiUyQyUyMnNlc3Npb25JZCUyMiUzQTE3NTI0NzA1ODk0NDglMkMlMjJvcHRPdXQlMjIlM0FmYWxzZSUyQyUyMmxhc3RFdmVudElkJTIyJTNBMTE3JTdE; MYJ_wig5buyoga=JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjJhZDJhMDYxNC0xZDczLTRlNzMtYTc1Yy1hZTlmOGU0ZmU3YjMlMjIlMkMlMjJ1c2VySWQlMjIlM0ElMjIxNDMwJTIyJTJDJTIycGFyZW50SWQlMjIlM0ElMjIxMjIlMjIlMkMlMjJzZXNzaW9uSWQlMjIlM0ExNzUyNDc0MTgzMDY2JTJDJTIyb3B0T3V0JTIyJTNBZmFsc2UlMkMlMjJsYXN0RXZlbnRJZCUyMiUzQTMyJTdE; JSESSIONID=37F034F761B441E5CBD0971675BDDFFB'
#     }
#     data = {
#         "createBeginTime": '',
#         "createEndTime": '',
#         "inquireType": 2,
#         "searchType": 'sku',
#         "searchContent": '',
#         "type": '',
#         "pageNo": 1,
#         "pageSize": 50
#     }
#     send = SendRequests()
#     res = send.execute_api_request(url=url, headers=headers, method=method, json=data)
#     print(res)
