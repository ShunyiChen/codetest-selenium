class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.status = False


# users = [User('admin', 'Admin-1234'),
#          User('Ivantong', 'ASDqwe123!'),
#          User('Ali_01', 'ASDqwe123!')]



users = [User('SADC_01', 'ASDqwe123!')]

# 读取填报模板文件
file_name = r'C:\\Users\\QD291NB\\Downloads\\KPI填报批量导出模板.xlsx'
generated_file_name = r'C:\\Users\\QD291NB\\Downloads\\generated.xlsx'