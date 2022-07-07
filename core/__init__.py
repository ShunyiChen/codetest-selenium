import time


def get_now_time():
    now = time.localtime()
    now_time = time.strftime("%Y-%m-%d %H:%M:%S", now)
    return now_time
