import unittest
import os

from lib import HTMLTestRunner
from logintests import LoginTests
from logouttests import LogoutTests

# 获取所有测试用例
login_tests = unittest.TestLoader().loadTestsFromTestCase(LoginTests)
logout_tests = unittest.TestLoader().loadTestsFromTestCase(LogoutTests)

# 取当前工作目录来保存输出报告
dir = os.getcwd()

# 创建TestSuite
smoke_tests = unittest.TestSuite([login_tests, logout_tests])

# 打开报告文件
outfile = open(dir + "\SmokeTestReport.html", "w", encoding='utf-8')

# 配置HTMLTestRunner选项
runner = HTMLTestRunner.HTMLTestRunner(stream=outfile,
                                       title='Test Report',
                                       description='Smoke Tests')

# 使用HTMLTestRunner运行TestSuite
runner.run(smoke_tests)

# TestSuite普通运行方法
# unittest.TextTestRunner(verbosity=2).run(smoke_tests)

