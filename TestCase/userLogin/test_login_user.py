import pytest


@pytest.fixture(scope="function")
def sql_session():
    #todo 连接数据库
    print("---tken")
    # yield
    #todo 关闭数据库
    print("---l;")

class TestLoginUser:


    def test_login(self,sql_session):
        print("---------")


