import requests

#该方法不加入参数usrtname、pwd原因是：所有的接口只需要同一个账号的token就可以了，因此为了避免调用时候的重复，除非是校验角色权限，否则用同一个方法

def get_header_by_user():
    username=""
    password=""
    request_url = "我是登陆接口的URL"
    resp = requests.post(request_url, json={"username": username, "password": password})
    header = {"Content-Type": "application/json",
              "Authorization": f"Bearer {resp.json()['access_token']}"}

    # 返回结果是个元祖，获取header只需要调用结果header[0]即可
    return header


