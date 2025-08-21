from locust import TaskSet, HttpUser, task, between


#HttpUser是HttpLocust重命名而来
class UserBehavior(HttpUser):
    #用户执行一个任务之后停留1-3秒
    wait_time = between(1,3)
    #每个用户启动之前执行
    def on_start(self):
        self.client.post("/login",json={"username":"admin","password":"12533167"})

    @task #点击首页
    def index(self):
        with self.client.get("/index.html", catch_response=True) as response:
            if response.text != "OK":
                response.failure("Got wrong response")
            elif response.elapsed.total_seconds() > 0.5:
                response.failure("Request took too long")

    @task(2) #task可以设置权重
    def logout(self):
        self.client.get("/logout")

class MyLocust():
    task_set=UserBehavior  #该 task_set 属性应该指向一个 TaskSet 定义用户行为的类
    min_wait = 4000  #用户执行任务之间等待时间的下界，单位：毫秒，默认值：1000
    max_wait = 10000
    host = "www.baidu.com"
    weight = 10 #用户被选中的概率，权重越大，被选中的机会就越大。默认值：10

'''
    使用dos运行：locust -f user_behavior.py文件，然后会弹出来一个窗口，模拟用户数量和每秒递增用户数即可。
'''

