import json
import logging
import re

from Common.handle_data.yaml_data_api import YamlDataApi

'''
利用正则和反射机制，把yaml或json文件中的函数变量替换成函数实际调用结果
'''


class YamlReplaceWithFuncResult(object):
    def __init__(self, reflex_obj=YamlDataApi()):
        # 传入反射机制所指向的类
        self.reflex_obj = reflex_obj

    def yaml_analysis(self, yaml_data_str):
        '''
        解析yaml中的函数，并将结果返回给yaml（比如token、cookie、content-type、根据账户得到的密码）
        :param yaml_data_str:
        :return:
        '''
        # 将输入的数据转化为字符串格式, 如果输入的数据已经是字符串格式, 则直接返回, 否则将其转化为JSON格式的字符串
        # yaml_data_str = yaml_data if isinstance(yaml_data_str, str) else json.dumps(yaml_data_str, ensure_ascii=False)

        # 循环处理yaml_data_str中的所有变量引用
        for _ in range(yaml_data_str.count('${')):
            if '${' in yaml_data_str and '}' in yaml_data_str:
                # 获取变量引用的开始位置
                start_index = yaml_data_str.index('${')
                # 获取变量引用的结束位置
                end_index = yaml_data_str.index('}', start_index)
                # 切片截取
                variable_data = yaml_data_str[start_index: end_index + 1]
                # 使用正则表达式提取函数名和参数
                match = re.match(r'\$\{(\w+)\((.*?)\)\}', variable_data)
                # 如果匹配成功, 则获取函数名和参数
                if match:
                    # 获取函数名和参数:（如：${read_yaml_data(user.name.0)}）  func_name, func_args = match.groups()
                    func_name = match.group(1)
                    func_args = match.group(2)
                    # 调用DebugTalk类中的相应方法, 并获取返回值
                    extract_data = getattr(self.reflex_obj, func_name)(*func_args)
                    # 将返回值替换到原始字符串中（下一次遍历的时候可以重新获取${，相当于每获一次，剪短一部分）
                    yaml_data_str = re.sub(re.escape(variable_data), str(extract_data), yaml_data_str)
        try:
            # 字符串解析为JSON对象
            data = json.loads(yaml_data_str)
        except json.JSONDecodeError:
            # 返回原始字符串
            data = yaml_data_str
        return data

    def yaml_analysis_execution(self, caseinfo):
        """
        解析并执行yaml文件中的测试用例
        Args:
         caseinfo (dict): 包含测试用例信息的yaml字典, 必须包含name、base_url、request和validation等关键字
        returns:
        """
        try:
            caseinfo_keys = dict(caseinfo).keys()
            # 校验yaml文件的一级关键字是否包含name、base_url、request、validation
            if 'name' in caseinfo_keys and 'base_url' in caseinfo_keys and 'request' in caseinfo_keys and 'validation' in caseinfo_keys:
                # 获取request字典的所有键
                request_keys = dict(caseinfo['request']).keys()
                # print(f'四个一级关键字: {caseinfo_keys}')
                # 校验二级关键字是否包含method、path
                if 'method' in request_keys and 'path' in request_keys:
                    # print(f'两个二级关键字: {request_keys}')
                    name = caseinfo['name']
                    # 替换base_url中的变量
                    base_url = self.replace.parse_replace(caseinfo['base_url'])
                    # 替换path中的变量,从request中移除path并获取其值
                    path = self.replace.parse_replace(caseinfo['request'].pop('path'))
                    # 拼接完整的请求URL
                    url = base_url + path
                    # 从request中移除method并获取其值
                    method = caseinfo['request'].pop('method')

                    # request下存在headers, 将其做解析并替换, 然后headers去除
                    headers = caseinfo['request'].get('headers', None)
                    if headers is not None:
                        try:
                            # 安全解析字符串（如果是字典/列表格式的字符串）
                            if isinstance(headers, str):
                                headers = ast.literal_eval(self.replace.parse_replace(headers))
                            # 更新并移除 headers
                            caseinfo['request']['headers'] = headers
                            caseinfo['request'].pop('headers', None)
                        except (SyntaxError, ValueError) as e:
                            print(f"解析 cookies 失败: {e}")

                    # request下存在cookies, 将其做解析并替换, 然后cookies去除
                    cookies = caseinfo['request'].get('cookies', None)
                    if cookies is not None:
                        try:
                            # 安全解析字符串（如果是字典/列表格式的字符串）
                            if isinstance(cookies, str):
                                cookies = ast.literal_eval(self.replace.parse_replace(cookies))
                            # 更新并移除 cookies
                            caseinfo['request']['cookies'] = cookies
                            caseinfo['request'].pop('cookies', None)
                        except (SyntaxError, ValueError) as e:
                            print(f"解析 cookies 失败: {e}")

                    # request下存在files, 将其做解析并替换, 然后files去除
                    files = caseinfo['request'].get('files', None)
                    if files is not None:
                        # 打开文件并更新request中的files
                        files = {key: open(value, 'rb') for key, value in files.items()}
                        caseinfo['request']['files'] = files
                        # 从request中移除files
                        caseinfo['request'].pop('files', None)

                    # 处理request中去除headers、cookies、files、path、method, 剩余一个请求体参数(data/json/params)参数类型和请求参数
                    param_type, request_params = None, None
                    # 遍历request中的参数类型
                    for param_type, params_params in caseinfo['request'].items():
                        if param_type in ['params', 'data', 'json']:
                            # 替换参数中的变量
                            request_params = self.replace.parse_replace(params_params)
                            # 更新request中的参数
                            caseinfo['request'][param_type] = request_params

                    # 执行请求
                    real_send = self.send_request.execute_request
                    # -------------- 新增 begin --------------
                    real_send = MockUtil.patch_if_needed(caseinfo, real_send)
                    response = real_send(name=name,
                                         method=method,
                                         url=url,
                                         headers=headers,
                                         cookies=cookies,
                                         files=files,
                                         **caseinfo['request'])
                    status_code, response_text = response.status_code, response.text
                    logging.info(f'接口实际返回结果: {response_text}')

                    # 在allure报告Test body显示内容
                    allure_info = {
                        '用例名称': name,
                        '基础地址': base_url,
                        '接口路径': path,
                        '请求方式': method,
                        'headers': allure_attach_dict_result(headers if headers else "无需headers"),
                        'Cookies': allure_attach_dict_result(cookies if cookies else "无需Cookies"),
                        '参数类型': param_type if param_type else "",
                        '请求参数': allure_attach_dict_result(request_params if request_params else "无需入参"),
                        '接口响应信息': allure_attach_dict_result(response.json())
                    }
                    for title, content in allure_info.items():
                        allure.attach(content, title, attachment_type=allure.attachment_type.JSON)

                    # 处理接口返回值提取
                    try:
                        # 存在extract, 将其做解析并替换
                        extract = caseinfo.get('extract', None)
                        # 如果extract变量不为空, 则表示需要提取单个数据
                        if extract is not None:
                            # 提取单个数据
                            self.extract.extract_data(extract, response_text)
                        # 存在extract_list, 将其做解析并替换
                        extract_list = caseinfo.get('extract_list', None)
                        # 如果extract_list变量不为空, 则表示需要提取数据列表
                        if extract_list is not None:
                            # 提取数据列表
                            self.extract.extract_data_list(extract_list, response_text)
                    except Exception as e:
                        logging.error(f'提取参数失败,错误信息:{e}, 请检查接口返回信息或表达式!')
                        raise

                    # 处理接口断言
                    finally:
                        # 存在validation, 将其做解析并替换
                        validation = self.replace.parse_replace(caseinfo.get('validation'))
                        # 调用assert对象的assert_result方法进行断言操作,
                        self.asserts.assert_result(validation, response.json(), status_code)
                else:
                    logging.error('测试文件中, 必须包含二级关键字: method、path')
            else:
                logging.error('测试文件中, 必须包含一级关键字: name、base_url、request、validation')
        except KeyError as ke:
            logging.error(f'缺少必要的键: {ke}')
        except Exception as e:
            logging.error(f'执行用例失败,错误信息: {e}')
            raise e
