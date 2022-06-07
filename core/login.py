import core
from conf import users

def login(username, password):
    url = 'http://localhost:8081/#/login'
    core.wd.get(url)
    core.time.sleep(1)
    element = core.wd.find_element_by_xpath("//input[@placeholder='账号']").send_keys(username)
    element = core.wd.find_element_by_xpath("//input[@placeholder='密码']").send_keys(password)
    element = core.wd.find_element_by_xpath("//img[@alt='']")
    data = element.screenshot_as_png
    # 百度OCR
    res = core.client.basicGeneral(data, {})
    print(res)
    # 取得OCR返回结果
    wr = res['words_result']
    code = wr[0]['words']
    print("code=",code)
    # 输入验证码
    element = core.wd.find_element_by_xpath("//input[@placeholder='验证码']").send_keys(code)
    # 点击登录按钮
    element = core.wd.find_element_by_tag_name('button')
    core.time.sleep(1)
    element.click()
    core.time.sleep(1)
    try:
        # 判断页面是否存在错误提示，如存在则返回错误元素
        element = core.wd.find_element_by_xpath("//p[@class='el-message__content']")
    except:
        return ''
    return element

def try10Times():
    for u in users.users:
        print(u.username, u.password)

