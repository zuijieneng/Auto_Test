import unittest
from htmltestreport import HTMLTestReport
from TestCase.test_login import TestLogin

# 创建套件实例
suite = unittest.TestSuite()
# 添加测试类，组装测试用例
# suite.a(unittest.makeSuite(TestLogin))
suite.addTest(TestLogin("test_login"))
# 创建报告实例
runner = HTMLTestReport("./report/report.html", description="gdc测试报告", title="测试报告")
runner.run(suite)
