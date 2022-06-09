import time
import threading
import os
from xml.dom.minidom import Element
from tkinter import *
from tkinter import Button, Tk, Frame, Label, DISABLED,ACTIVE, PhotoImage, LEFT, messagebox
from aip import AipOcr
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

wd = None
is_paused = False

def initialize():
    global ser
    global client
    global wd
    # 加载chrome驱动
    ser = Service(r'C:\Users\QD291NB\Downloads\selenium\101.4951.64\chromedriver_win32\chromedriver.exe')
    # 实现不自动关闭的重点
    option = webdriver.ChromeOptions()
    option.add_experimental_option("detach", True)
    wd = webdriver.Chrome(service=ser, options=option)
    # 创建ocr客户端
    client = AipOcr("25675193", "aq4ULqZRRzIZHglVpVhbtjDK", "SvKmQjurRTEkKNVqIGlje8TH5kKnp8cl")


def destroy():
    # 退出webdriver
    if wd is not None:
        wd.quit()


