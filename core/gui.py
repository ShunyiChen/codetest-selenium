import core
from core import Tk, Button, Frame, Label, DISABLED, ACTIVE, PhotoImage, LEFT, messagebox, capes, threading, time
from conf import users

u_count = 0
t = None
root = Tk()
photo = PhotoImage(file=r"res/pause.png")
photoimage = photo.subsample(10, 10)

photo_start = PhotoImage(file=r"res/start.png")
photo_start_image = photo_start.subsample(10, 10)

photo_resume = PhotoImage(file=r"res/resume.png")
photo_resume_image = photo_resume.subsample(10, 10)

photo_quit = PhotoImage(file=r"res/quit.png")
photo_quit_image = photo_quit.subsample(10, 10)

photo_report = PhotoImage(file=r"res/report.png")
photo_report_image = photo_report.subsample(10, 10)


class GUI(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.btnReport = None
        self.btnQuit = None
        self.btnStart = None
        self.labelShowContent = None
        self.label = None
        self.btnPause = None
        self.master = master
        self.pack()
        self.initComponents()

    def initComponents(self):
        self.label = Label(self, text="执行状态: 未开始", bg="MediumTurquoise", fg="white", padx="10", font=("黑体", 15))
        self.label.pack(side="top")

        self.labelShowContent = Label(self, text="--", padx="10")
        self.labelShowContent.pack(side="top")

        self.btnStart = Button(self, padx="10")
        self.btnStart["text"] = "开始"
        self.btnStart["image"] = photo_start_image
        self.btnStart["compound"] = LEFT
        self.btnStart["command"] = start
        self.btnStart.pack(side="left")

        self.btnPause = Button(self, text="暂停", image=photoimage, compound=LEFT, padx="10",
                               command=pause)
        self.btnPause.pack(side="left")
        self.btnPause.config(state=DISABLED)

        self.btnQuit = Button(self, text="退出", image=photo_quit_image, compound=LEFT, padx="10",
                              command=quit)
        self.btnQuit.pack(side="left")

        self.btnReport = Button(self, text="报告", image=photo_report_image, compound=LEFT, padx="10",
                                command=report)
        self.btnReport.pack(side="left")


def launch():
    root.geometry("420x80+30+140")
    root.title('Selenium自动化控制台')
    root.resizable(False, False)
    # tk窗口放到最前端显示
    root.attributes("-topmost", True)
    global gui
    gui = GUI(master=root)
    root.mainloop()


def quit():
    # 关闭Webdriver
    core.destroy()
    # 关闭GUI界面
    root.destroy()


def report():
    print('report---')


def start():
    # 参数表示用户可最大登录次数
    global t
    t = threading.Thread(target=try_logining_for_several_times, args=(1,))
    t.start()
    # global t
    # t = job.Job(target=try_logining_for_several_times, args=(1,))
    # t.start()
    gui.btnStart.config(state=DISABLED)
    gui.btnPause.config(state=ACTIVE)


def pause():
    core.is_paused = True
    print('Paused---', core.is_paused)
    # messagebox.showinfo("提示", "继续！")
    gui.btnPause.config(state=DISABLED)


def try_logining_for_several_times(times):
    global u_count
    u_count = 0
    print("times=", times, "u_count=", u_count)
    gui.label["text"] = "执行状态: 正在执行"
    # 初始化加载chrome驱动、创建百度OCR客户端
    core.initialize()
    loop_users(times)
    done()


def loop_users(times):
    # 遍历登录人员列表
    global u_count
    for i in range(0, len(users.users)):
        u = users.users[i]
        gui.labelShowContent["text"] = str(u_count) + "/" + str(len(users.users)) + " 当前用户：" + u.username
        if not u.status:
            # time.sleep(1)
            set_anchor_point(1)
            # 每个用户最多尝试登录10次
            count = 0
            while count < times:
                # 登录CapES
                element = capes.login(u.username, u.password)
                if element != '':
                    print("登录第" + str(count) + "次失败，尝试重新登录")
                    count = count + 1
                else:
                    u.status = True
                    print("登录成功")
                    u_count = u_count + 1
                    gui.labelShowContent["text"] = str(u_count) + "/" + str(len(users.users)) + " 当前用户：" + u.username
                    # time.sleep(2)
                    set_anchor_point(2)
                    capes.downloadTemplate()

                    # 用随机数更新excel内容
                    capes.updateExcel()
                    # 批量提交
                    capes.submitExcel()

                    # 退出CapES
                    capes.logout()
                    # time.sleep(1)
                    set_anchor_point(1)
                    break

            if count == times:
                # 交给控制台处理
                # pass
                msg = messagebox.askquestion("提示", "登录次数已满 Yes-重新登录 No-直接跳过")
                print("count=", count, "times=", times, "msg=", msg)
                if msg == "yes":
                    loop_users(times)
                    break
                else:
                    pass

                    # gui.btnPause.config(state=DISABLED)
                    # gui.btnResume.config(state=ACTIVE)

    print("循环结束")


def done():
    # core.destroy()
    gui.label["text"] = "执行状态: 已完成"
    messagebox.showinfo("完成提示", "执行完成!")
    gui.btnPause.config(state=DISABLED)
    print("Done")


def set_anchor_point(sleep_time):
    if core.is_paused:
        messagebox.showinfo("暂停提示", "当前线程已暂停，点击”OK“继续执行。")
        core.is_paused = False
        gui.btnPause.config(state=ACTIVE)
    time.sleep(sleep_time)
