import time
import unittest

from selenium.common import TimeoutException
from selenium.webdriver import Keys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from aip import AipOcr
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class LoginTests(unittest.TestCase):
    # 类级别的测试前置方法
    @classmethod
    def setUpClass(cls):
        print("----setUpClass")

    # 测试前置方法
    def setUp(self):
        print("----setUp")
        # 初始化百度OCR服务连接
        self.aipocr = AipOcr("25675193", "aq4ULqZRRzIZHglVpVhbtjDK", "SvKmQjurRTEkKNVqIGlje8TH5kKnp8cl")
        # 加载驱动
        ser = Service(r'C:\Users\QD291NB\Downloads\selenium\103.0.5060.53\chromedriver_win32\chromedriver.exe')
        # 实现不自动关闭的重点
        option = webdriver.ChromeOptions()
        option.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(service=ser, options=option)
        # 设置隐式最大等待时间为10秒
        self.driver.implicitly_wait(10)
        # 浏览器最大化
        self.driver.maximize_window()
        # 打开网址
        url = 'http://localhost:8081/#/login'
        self.driver.get(url)

    # Case1:当验证码输入为空的情况，登录失败
    def test_login_failure(self):
        # 定位用户名文本框
        self.user_name_field = self.driver.find_element(By.CLASS_NAME, "el-input__inner")
        # 清除文本框内容
        self.user_name_field.send_keys(Keys.CONTROL + "a")
        self.user_name_field.send_keys(Keys.DELETE)
        # 输入用户名
        self.user_name_field.send_keys("admin")

        # 定位密码文本框
        self.pass_field = self.driver.find_element(By.XPATH, "//input[@placeholder='密码']")
        # 清除文本框内容
        self.pass_field.send_keys(Keys.CONTROL + "a")
        self.pass_field.send_keys(Keys.DELETE)
        # 输入密码
        self.pass_field.send_keys("Admin-1234")

        # 定位登录按钮
        self.login_button = self.driver.find_element(By.TAG_NAME, 'button')
        # 点击按钮
        self.login_button.click()

        # warning_msg = self.driver.find_element(By.CLASS_NAME, "el-form-item__error")
        msg_content = self.driver.find_element(By.XPATH, "//div[@class='el-form-item__error']")
        # 强制等待
        time.sleep(5)

        self.assertEqual("出错了", msg_content.text, "错误原因：提示信息不一致")

    # Case2:当用户名、密码、验证码都输入正确的情况，则登录成功
    def test_login_success(self):
        count = 0
        # 允许最大登录次数
        times = 10
        while count < times:
            login_user_name = self.login()
            if login_user_name == '':
                count += 1
                print("登录失败", count, "次")
            else:
                self.assertEqual("admin", login_user_name, "错误原因：登录用户名与主页显示名称不符。")
                break

    def login(self):
        # 定位用户名文本框
        self.user_name_field = WebDriverWait(self.driver, 3).until(
            expected_conditions.visibility_of_element_located(
                (By.CSS_SELECTOR, "input[placeholder='账号'][type='text']")))
        # 清除文本框内容
        self.user_name_field.send_keys(Keys.CONTROL + "a")
        self.user_name_field.send_keys(Keys.DELETE)
        # 输入用户名
        self.user_name_field.send_keys("admin")

        # 定位密码文本框
        self.pass_field = self.driver.find_element(By.XPATH, "//input[@placeholder='密码']")
        # 清除文本框内容
        self.pass_field.send_keys(Keys.CONTROL + "a")
        self.pass_field.send_keys(Keys.DELETE)
        # 输入密码
        self.pass_field.send_keys("Admin-1234")

        # 定位验证码图片
        self.code = self.driver.find_element(By.XPATH, "//img[@alt='']")
        # 取得验证码图片
        data = self.code.screenshot_as_png
        # 把图片传入百度OCR接口
        res = self.aipocr.basicGeneral(data, {})
        # 返回ORC识别结果
        wr = res['words_result']
        # 获取结果中words属性值
        code = wr[0]['words']
        print("识别号码 ", code)
        # 定位验证码文本框
        self.code_field = self.driver.find_element(By.XPATH, "//input[@placeholder='验证码']")
        # 清除文本框内容
        self.code_field.send_keys(Keys.CONTROL + "a")
        self.code_field.send_keys(Keys.DELETE)
        # 输入验证码
        self.code_field.send_keys(code)
        # 定位登录按钮
        self.login_button = self.driver.find_element(By.TAG_NAME, 'button')
        # 点击按钮
        self.login_button.click()

        try:
            # 判断是否获取到人名菜单
            menu = WebDriverWait(self.driver, 3).until(
                expected_conditions.visibility_of_element_located((By.CSS_SELECTOR,
                                                                   "span[role='button'][aria-haspopup='list']")))
            return menu.text
        except TimeoutException:
            pass
        return ''

    # 测试后置方法
    def tearDown(self):
        print("----tearDown")
        self.driver.quit()

    # 类级别的测试后置方法
    @classmethod
    def tearDownClass(cls):
        print("----tearDownClass")
