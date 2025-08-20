'''
一个locust类代表一个用户（或者代表一群蝗虫，如果有的话）；
locust 将为每个正在模拟的用户生成 locust 类的一个实例。
locust 类通常应定义一些属性。
一个用户行为类，要继承TaskSet类，表示一个任务集
on_start：前置方法(前置任务)，在所有任务之前调用
on_stop：后置方法(后置任务)，当任务集停止时调用
tasks：用来添加任务，它是一个dict类型，key表示任务的方法名，value表示挑选执行的权重，数值越大执行频率越高
'''
from locust import HttpUser

'''
模拟用户发起请求
'''
