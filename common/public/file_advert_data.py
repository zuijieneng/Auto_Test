import json
import csv

import openpyxl
import pandas

from config import BASE_FILE_DIR


def get_json_to_list_data(file_name):
    new_list = []
    with open(BASE_FILE_DIR.joinpath(file_name), 'r',
              encoding='utf-8') as f:  # with open("../test_data/"+file_name, 'r', encoding='utf-8') as f:
        data = json.load(f)
        for i in data:
            username = i.get("username")
            password = i.get("password")
            expect = i.get("expect")
            new_list.append((username, password, expect))
    print(new_list)
    return new_list


def get_csv_to_list_data(file_name):
    new_list = []
    with open(BASE_FILE_DIR.joinpath(file_name), 'r', encoding='utf-8') as f:
        reader_data = csv.reader(f)
        # 跳过首行数据
        next(reader_data)
        for row in reader_data:
            username = row[0]
            password = row[1]
            expect = row[2]
            new_list.append((username, password, expect))
    return new_list


def get_excel_data(file_name):
    new_list = []
    with open(BASE_FILE_DIR.joinpath(file_name), 'r', encoding='utf-8') as f:
        # 打开工作簿
        workbook = openpyxl.load_workbook(filename=BASE_FILE_DIR.joinpath(file_name))
        # 选择要操作的工作表
        sheet = workbook.active
        # 读取数据:先读取行再读取列
        for i in range(2,sheet.max_row+1):  # 从第二行开始读取，表头不要
            row_list = []
            for j in range(1,sheet.max_column+1):
                row_list.append(sheet.cell(row=i, column=j).value)
            new_list.append(row_list)
        print(new_list)

# def get_excel_data(file_name, sheet_name, skiprows):
#     new_list = []
#     rul=BASE_FILE_DIR.joinpath(file_name)
#     print(rul)
#     df = pandas.read_excel(rul, sheet_name=sheet_name, skiprows=skiprows)
#     print(df)
#     for i in df.index.values:
#         print(i)
#     return new_list


# 把字典、列表转换成json数据，并写到文件中
def write_json_date(data, filename):
    with open(BASE_FILE_DIR.joinpath(filename), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)  # 关闭 ASCII 编码强制转换、缩进 2 个空格


def wirte_device_csv_data(data, file_name):
    # 生成 1000 条测试账号（用户名：test_001 到 test_1000，密码：123456+序号）
    with open(BASE_FILE_DIR.joinpath('users.csv'), 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # 写入表头
        writer.writerow(['node_code', 'code', 'name', 'device_type_name', 'name1', 'name2', 'name3', 'name4'])
        # 写入数据
        for i in range(1, 1001):
            node_code = f"node_code_{i:03d}"  # 格式化为 test_001, test_002...
            code = f"deivce_code_{i}"
            name = f"name{i}"
            device_type_name = f"XX"
            name = f"name{i}"
            writer.writerow([node_code, code, name])

