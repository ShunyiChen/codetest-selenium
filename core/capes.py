import conf.users
import core


def login(username, password):
    # 浏览器窗口最大化
    core.wd.maximize_window()
    url = 'http://localhost:8081/#/login'
    core.wd.get(url)
    core.time.sleep(1)
    core.wd.find_element_by_xpath("//input[@placeholder='账号']").send_keys(username)
    core.wd.find_element_by_xpath("//input[@placeholder='密码']").send_keys(password)
    element = core.wd.find_element_by_xpath("//img[@alt='']")
    data = element.screenshot_as_png
    # 百度OCR
    res = core.client.basicGeneral(data, {})
    print(res)
    # 取得OCR返回结果
    wr = res['words_result']
    code = wr[0]['words']
    print("识别号码 ", code)
    # 输入验证码
    core.wd.find_element_by_xpath("//input[@placeholder='验证码']").send_keys(code)
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


def logout():
    element = core.wd.find_element_by_xpath(
        "//ul[@class='site-navbar__menu site-navbar__menu--right el-menu--horizontal el-menu']").click()
    core.time.sleep(1)
    element = core.wd.find_element_by_xpath("//li[text()='退出']").click()
    core.time.sleep(1)
    element = core.wd.find_element_by_xpath(
        "//button[@class='el-button el-button--default el-button--small el-button--primary ']").click()


def downloadTemplate():
    print("进入KPI填报界面")
    element = core.wd.find_element_by_xpath("//div[@class='el-scrollbar__view']/ul[@role='menubar']/li[2]").click()
    core.time.sleep(1)
    # 点击填报年度下拉框
    element = core.wd.find_element_by_xpath(
        "//div[@class='el-form-item__content']/div[@class='el-select el-select--medium']/div[@class='el-input el-input--medium el-input--suffix']").click()
    core.time.sleep(1)
    # 选择“2021FY”
    element = core.wd.find_element_by_xpath("//li[2]/span[text()='2021FY']").click()
    core.time.sleep(1)
    # 点击清除填报期下拉框
    element = core.wd.find_element_by_xpath(
        "//div[@class='el-col el-col-7']/div[@class='el-form-item el-form-item--medium']/div[@class='el-form-item__content']/div[@class='el-select el-select--medium']/div[@class='el-input el-input--medium el-input--suffix']/span[@class='el-input__suffix']/span[@class='el-input__suffix-inner']").click()
    core.time.sleep(1)
    # 点击查询按钮
    element = core.wd.find_element_by_xpath(
        "//button[@class='el-button el-button--primary el-button--medium']/span[text()='查询']").click()
    core.time.sleep(1)
    # 点击批量导出按钮
    element = core.wd.find_element_by_xpath(
        "//button[@class='el-button fillBt el-button--primary el-button--medium']/span[text()='批量导出']").click()
    core.time.sleep(10)


def updateExcel():
    print("更新excel内容")
    file_path = core.os.path.join('./', conf.users.file_name)
    wb = core.load_workbook(file_path)
    # sheet = wb.get_sheet_names()
    # print(sheet)
    w1 = wb.get_sheet_by_name('Sheet1')
    # print(w1)
    rows = w1.max_row
    for i in range(1, rows):
        # 单位列
        unit = w1["H"+str(i+1)].value
        if unit == '吨':
            w1["G" + str(i + 1)] = core.random.randint(10000,100000)
        elif unit == '标准立方米':
            w1["G" + str(i + 1)] = core.random.randint(10000,100000)
        elif unit == '千瓦时':
            w1["G" + str(i + 1)] = core.random.randint(50000,1000000)
        elif unit == '万元':
            w1["G" + str(i + 1)] = round(core.random.uniform(500.01,1000.99),2) #保留两位小数

    wb.save(conf.users.generated_file_name)
    print('excel更新完成')
    core.time.sleep(1)



def submitExcel():
    print("提交excel内容")
    # core.time.sleep(3)
    # 点击批量导出按钮
    # element = core.wd.find_element_by_xpath(
    #     "//button[@class='el-button fillBt el-button--primary el-button--medium']/span[text()='批量导入']").click()

    element = core.wd.find_element_by_name('file')
    element.send_keys(conf.users.generated_file_name)

    core.time.sleep(15)
    # 导入成功后点确定
    element = core.wd.find_element_by_xpath(
        "//button[@class='el-button el-button--default el-button--small el-button--primary ']").click()

    core.time.sleep(3)
    # 批量提交
    element = core.wd.find_element_by_xpath(
        "//button[@class='el-button fillBt el-button--primary el-button--medium']/span[text()='批量提交']").click()
    # 提交暂存数据后点确定
    element = core.wd.find_element_by_xpath(
        "//button[@class='el-button el-button--default el-button--small el-button--primary ']").click()

    core.time.sleep(15)

    print("提交excel完成")