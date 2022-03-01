
import time
from xml.dom.minidom import Element
from aip import AipOcr 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
# from selenium.webdriver import By

ser = None
client = None
wd = None

def create():
    global ser
    global client
    global wd

    # 加载chrome驱动
    ser = Service(r'C:\Users\QD291NB\Downloads\selenium\chromedriver_win32\chromedriver.exe')
    # 实现不自动关闭的重点
    option = webdriver.ChromeOptions()
    option.add_experimental_option("detach", True)
    # 创建ocr客户端
    client = AipOcr("25675193", "aq4ULqZRRzIZHglVpVhbtjDK", "SvKmQjurRTEkKNVqIGlje8TH5kKnp8cl")
    wd = webdriver.Chrome(service=ser,options=option)

def destroy():
    wd.quit()

def login(username, password): 
    wd.get('http://localhost:8081/#/login')
    time.sleep(1)
    element = wd.find_element_by_xpath("//input[@placeholder='账号']").send_keys(username)
    element = wd.find_element_by_xpath("//input[@placeholder='密码']").send_keys(password)
    element = wd.find_element_by_xpath("//img[@alt='']")
    data = element.screenshot_as_png
    # 百度OCR
    res = client.basicGeneral(data, {})
    print(res)
    # 取得OCR返回结果
    wr = res['words_result']
    code = wr[0]['words']
    print("code=",code)
    # 输入验证码
    element = wd.find_element_by_xpath("//input[@placeholder='验证码']").send_keys(code)
    # 点击登录按钮
    element = wd.find_element_by_tag_name('button')
    time.sleep(1)
    element.click()
    time.sleep(1)
    try:
        # 判断页面是否存在错误提示，如存在则返回错误元素
        element = wd.find_element_by_xpath("//p[@class='el-message__content']")
    except:
        return ''
    return element

def tryLogin(times): 
    count = 0
    while(count < times):
        element = login('admin', 'Admin-1234')
        if element != '':
            print("The count is:",count, "失败")
            count = count + 1
        else:
            print("count=",count,"成功！")
            count = 10;
            dashboard()

def dashboard(): 
    print("进入Dashboard")
    element = wd.find_element_by_xpath("//div[@class='el-scrollbar__view']/ul[@role='menubar']/li[5]").click()
    time.sleep(1)
    element = wd.find_element_by_xpath("//div[@class='el-scrollbar__view']/ul[@role='menubar']/li[5]/ul[1]/li[2]").click()
    time.sleep(3)
    logout()

def logout():
    print("准备Logout")
    element = wd.find_element_by_xpath("//ul[@class='site-navbar__menu site-navbar__menu--right el-menu--horizontal el-menu']").click()
    time.sleep(1)
    element = wd.find_element_by_xpath("//li[text()='退出']").click()
    time.sleep(1)
    element = wd.find_element_by_xpath("//button[@class='el-button el-button--default el-button--small el-button--primary ']").click()
    time.sleep(2)

if __name__ == '__main__':
    create()
    # 尝试登录10次为止
    tryLogin(10)
    # 推出webdriver
    destroy()
    