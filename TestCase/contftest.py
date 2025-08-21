import pytest


@pytest.fixture(scope="module")
def sql_session():
    #todo 连接数据库
    print("---tken")
    yield
    #todo 关闭数据库
    print("---l;")
