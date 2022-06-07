
from core import Tk,Button,Frame,Label,DISABLED,PhotoImage,LEFT,messagebox
from core import login

root = Tk()
photo = PhotoImage(file = r"res/pause.png")
photoimage = photo.subsample(10, 10)

photo_start = PhotoImage(file = r"res/start.png")
photo_start_image = photo_start.subsample(10, 10)

photo_resume = PhotoImage(file = r"res/resume.png")
photo_resume_image = photo_resume.subsample(10, 10)

photo_quit = PhotoImage(file = r"res/quit.png")
photo_quit_image = photo_quit.subsample(10, 10)

photo_report = PhotoImage(file = r"res/report.png")
photo_report_image = photo_report.subsample(10, 10)

class GUI(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.initComponents()

    def initComponents(self):
        self.label = Label(self, text="执行进度:", bg="grey", fg="white", padx="10")
        self.label.pack(side="top")

        self.labelShowContent = Label(self, text="1/15 admin", padx="10")
        self.labelShowContent.pack(side="top")

        self.btnStart = Button(self, padx="10")
        self.btnStart["text"] = "开始"
        self.btnStart["image"] = photo_start_image
        self.btnStart["compound"] = LEFT
        self.btnStart["command"] = self.start
        self.btnStart.pack(side="left")

        self.btnPause = Button(self, text="暂停", image = photoimage, compound = LEFT, padx="10", command=self.pause)
        self.btnPause.pack(side="left")

        self.btnResume = Button(self, text="继续", padx="10", image = photo_resume_image, compound = LEFT, command=self.resume)
        self.btnResume.pack(side="left")
        # self.btnResume.pack_forget()

        self.btnQuit = Button(self, text="退出", image = photo_quit_image, compound = LEFT, padx="10", command=root.destroy)
        self.btnQuit.pack(side="left")

        self.btnReport = Button(self, text="报告", image = photo_report_image, compound = LEFT, padx="10", command=self.resume)
        self.btnReport.pack(side="left")


    def start(self):
        self.btnStart.config(state=DISABLED)
        print('started----')
        login.try10Times()

    def pause(self):
        print('Pause---')
        messagebox.showinfo("提示", "完成！")

    def resume(e):
        print('resume---')


def launch():
    root.geometry("450x80+30+30")
    root.title('Selenium自动化控制台')
    pane = GUI(master=root)
    root.mainloop()


