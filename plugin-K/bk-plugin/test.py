import pyautogui
import time
import cv2
import numpy as np
from pynput import mouse

# 鼠标移动到左上角抛出异常
pyautogui.FAILSAFE = True

# 输出屏幕宽，高
width, height = pyautogui.size()
print(width,height)

# 使用cv2模块获取截图在屏幕位置
def cv_get_screen_area():
    template = cv2.imread('all.png')
    screen = cv2.imread("1.png")

    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

    w,h = screen_gray.shape[::-1]

    res = cv2.matchTemplate(template_gray,screen_gray,cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):
        center = center = (pt[0] + w // 2, pt[1] + h // 2)
        print(center)
        print(pt)

        pyautogui.moveTo(center)
        break
    else:
        print("Templat not fount on the screen")

# 使用pyautogui模块获取截图在屏幕位置
def gui_get_screen_area():
    # 截图路径
    sceenpath = "1.png"

    # 查找截图在屏幕中的位置
    location = pyautogui.locateOnScreen(sceenpath)
    if location:
        center = pyautogui.center(location)
        pyautogui.moveTo(center)

def auto_click(x,y):
    time.sleep(3)
    pyautogui.click(x,y,2)

# 鼠标点击输出点击位置坐标
def get_screen_area():
    global last_click
    current_click = pyautogui.position()

    if current_click != last_click:
        currentMouseX, currentMouseY = pyautogui.position()
        print(currentMouseX, currentMouseY)
        last_click = current_click

# 鼠标点击监听事件
def mouse_click():
    with mouse.Listener(on_click=get_screen_area) as listener:
        listener.join()

# 自动点击创建索引集
def auto_index():
    global num
    pyautogui.click(358,316,1)
    time.sleep(1)
    pyautogui.click(494,321,1)
    pyautogui.write(f'log{num}',1)
    pyautogui.click(527, 366, 1)
    pyautogui.moveTo(560,493,2)
    pyautogui.scroll(-500)
    pyautogui.click(542,594,2)
    pyautogui.click(514,524,2)
    pyautogui.click(549,626,1)
    pyautogui.click(494,581,2)
    pyautogui.click(587,404,2)
    time.sleep(1)
    pyautogui.click(608,473,1)
    pyautogui.click(894,831,1)
    time.sleep(1)
    pyautogui.click(386,672,1)
    pyautogui.scroll(-500)
    time.sleep(1)
    pyautogui.click(332,941,1)
    num+=1

if __name__ == '__main__':
    # 点击获取对应点击位置，获取位置后注释即可
    # time.sleep(3)
    # last_click = None
    # mouse_click()

    #自动创建索引集
    time.sleep(3)
    num = 16
    while num < 72:
        time.sleep(5)
        auto_index()


