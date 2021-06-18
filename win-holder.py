__version__ = '0.1.0'
"""
# config 为了控制打包体积，必须创建python虚拟环境
pipenv shell
pipenv install psutil pyautogui pynput pyinstaller

# build in pipenv shell -w 隐藏控制台 -F 打包成一个exe，会有两个process
pyinstaller.exe -Fw --icon=icon.ico --hidden-import "pynput.keyboard._win32" --hidden-import "pynput.mouse._win32" ./win-holder.py

# process name
win-holder.exe

"""
import pyautogui, time, datetime as dt, os, psutil, random
from pynput import keyboard, mouse

STARTUP_TIME = dt.datetime.now()
pyautogui.FAILSAFE = False
PROC_NAME = 'win-holder.exe'
keybord_mouse_triggered_latest_time = 0.0  # 最近一次键盘触发时间
detect_interval_seconds = 59


def mouse_move_listening():
    """监听鼠标移动"""

    def on_move(x, y):
        """更新当前数据位置"""
        global keybord_mouse_triggered_latest_time
        keybord_mouse_triggered_latest_time = time.time()

    listener = mouse.Listener(on_move=on_move)
    listener.start()


def keyboard_press_listening():
    """监听键盘触发"""

    def on_press(key):
        """任意键盘按下时，更新键盘触发时间"""
        print(f"key pressed = {key}")
        global keybord_mouse_triggered_latest_time
        keybord_mouse_triggered_latest_time = time.time()

    listener = keyboard.Listener(on_press=on_press, on_release=lambda key: None)
    listener.start()


def keybord_mouse_not_triggered_in_interval():
    """等候期间，键盘或鼠标是否被动过"""
    global keybord_mouse_triggered_latest_time
    cur_time = time.time()
    return cur_time - keybord_mouse_triggered_latest_time > detect_interval_seconds


def kill_exists_process():
    """kill the same task in background that start before"""
    for p in psutil.process_iter():
        try:
            pinfo = p.as_dict(attrs=['pid', 'name', 'create_time'])
            pname = pinfo['name']
            pid = pinfo['pid']
            create_time = dt.datetime.fromtimestamp(pinfo['create_time'])
            # pyinstaller有一个bootloader进程，所以会看到两个$PROC_NAME,不做时间间隔判断会kill掉当前bootloader进程
            if PROC_NAME in pinfo['name'].lower() and (STARTUP_TIME - create_time).seconds > 5:
                print(f"kill the process={pname}, pid={pid}, created_at={create_time.strftime('%Y-%m-%d %H:%M:%S.%f')}")
                os.system(f'taskkill /F /PID {pid}')
        except:
            pass


screen_w, screen_h = pyautogui.size()
kill_exists_process()
keyboard_press_listening()
mouse_move_listening()
while True:
    PM21 = dt.datetime.now().replace(hour=21, minute=30, second=0, microsecond=0)
    AM8 = dt.datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)
    if (dt.datetime.now() > PM21 or dt.datetime.now() < AM8) and \
            keybord_mouse_not_triggered_in_interval():
        cur_x, cur_y = pyautogui.position()
        x, y = cur_x + random.uniform(-200, 200), cur_y + random.uniform(-200, 200)
        pyautogui.moveTo(x, y)
        time.sleep(3)
        pyautogui.rightClick((2000, 1000))
        print(f"mouse move to x={x},y={y}")
        print(f"在{detect_interval_seconds}s内鼠标和键盘没有触发，自动触发了鼠标右键")

    time.sleep(detect_interval_seconds)