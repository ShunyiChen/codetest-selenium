import time
import os
from xml.dom.minidom import Element
from tkinter import *
from tkinter import Button, Tk, Frame, Label, DISABLED,PhotoImage,LEFT,messagebox
from aip import AipOcr
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

def init():
    global ser
    global client
    global wd

    # 加载chrome驱动
    ser = Service(r'C:\Users\QD291NB\Downloads\selenium\101.4951.64\chromedriver_win32\chromedriver.exe')
    # 实现不自动关闭的重点
    option = webdriver.ChromeOptions()
    option.add_experimental_option("detach", True)
    # 创建ocr客户端
    client = AipOcr("25675193", "aq4ULqZRRzIZHglVpVhbtjDK", "SvKmQjurRTEkKNVqIGlje8TH5kKnp8cl")
    wd = webdriver.Chrome(service=ser, options=option)