import threading
import tkinter
from tkinter import Tk, PhotoImage, Frame, Label, Button, LEFT, DISABLED, ACTIVE, messagebox

from core.capes import fill_data, driver_quit, users, start_time, end_time, get_start_time, get_end_time

u_count = 0
t = None
root = Tk()

photo_start = PhotoImage(file=r"res/start.png")
photo_start_image = photo_start.subsample(10, 10)

photo_quit = PhotoImage(file=r"res/quit.png")
photo_quit_image = photo_quit.subsample(10, 10)

photo_report = PhotoImage(file=r"res/report.png")
photo_report_image = photo_report.subsample(10, 10)


class GUI(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.btn_view_report = None
        self.btn_terminate = None
        self.btn_start = None
        self.label_show_progress = None
        self.label = None
        self.master = master
        self.pack()
        self.initComponents()

    def initComponents(self):
        self.label = Label(self, text="运行状态: 未开始", bg="MediumTurquoise", fg="white", padx="10", font=("黑体", 15))
        self.label.pack(side="top")

        self.label_show_progress = Label(self, text="0/"+str(len(users)), padx="10")
        self.label_show_progress.pack(side="top")

        self.btn_start = Button(self, padx="10")
        self.btn_start["text"] = "开始"
        self.btn_start["image"] = photo_start_image
        self.btn_start["compound"] = LEFT
        self.btn_start["command"] = start
        self.btn_start.pack(side="left")

        self.btn_terminate = Button(self, text="终止", image=photo_quit_image, compound=LEFT, padx="10",
                              command=terminate)
        self.btn_terminate.pack(side="left")

        self.btn_view_report = Button(self, text="查看报告", image=photo_report_image, compound=LEFT, padx="10",
                                command=view_report)
        self.btn_view_report.pack(side="left")


def launch():
    root.geometry("330x80+5+340")
    root.title('Selenium自动化控制台')
    root.resizable(False, False)
    # tk窗口放到最前端显示
    root.attributes("-topmost", True)
    global gui
    gui = GUI(master=root)
    root.mainloop()


def start():
    # 参数表示用户可最大登录次数
    global t
    t = threading.Thread(target=fill_data, args=(update_status_label,update_progress_label,))
    t.start()
    gui.btn_start.config(state=DISABLED)
    update_status_label("已开始")


def terminate():
    update_status_label("正在终止中")
    # 关闭Webdriver
    driver_quit()
    # 关闭GUI界面
    root.destroy()


def view_report():
    popup = tkinter.Toplevel(root)
    popup.wm_title("报告内容")
    popup.geometry("+350+250")

    text = tkinter.Text(popup)
    text.pack()

    text.tag_config('mytag', elide=True)
    # text.insert('end', "This text is non-elided.\r\nThis text is non-elided")
    logs = "开始时间："+get_start_time()+"\r\n"+"结束时间："+get_end_time()+"\r\n\r\n"
    for u in users:
        status = u.complete is True and 'Success' or 'Fail'
        logs += u.username+"\t------["+status+"]\r\n"
    text.insert('end', logs)
    text.tag_add('mytag', '-1.13', '-1.17')
    tkinter.Button(popup, text="Okay", command=popup.destroy).pack()


def update_status_label(status):
    gui.label["text"] = '运行状态: '+status


def update_progress_label(progress):
    gui.label_show_progress["text"] = progress