import jsonschema

# 准备校验规则 int、number、str、array、null、object、boolean
schema = {
    "type": "object",
    "properties": {
        "success": {"type": "boolean"},
        "code": {"type:": "integer"},
        "message": {"type": "string"},
        "money": {"const": 100},  # 确定值
        "address": {"type": "null"},
        "phone": {"pattern": "^[0-9]{11}$"},  # 模式匹配
        "luckyNumber": {"type": "array"},
        "data": {
            "type": "object",
            "properties": {
                "age": {"type": "integer"},
                "isFlag": {"const": False}
            },
            "required": ["age"]
        }
    },
    "required": ["success", "code", "message", "money", "address", "luckyNumber"]
}

# 准备测试数据
data = {
    "success": True,
    "code": 10000,
    "message": "操作成功",
    "money": 6.66,
    "address": None,
    "data": {
        "name": "tom"
    },
    "luckyNumber": [6, 8, 9]
}

# 调用方法进行校验
res = jsonschema.validate(instance=data, schema=schema)
print(res)
