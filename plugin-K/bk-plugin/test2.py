import cv2
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

# 初始化WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# 目标URL
url = 'https://xxx'  # 这里替换为你的目标URL
driver.get(url)

# 获取页面截图
sleep(12)
screenshot_path = 'screenshot.png'
driver.save_screenshot(screenshot_path)

# 解析截图
image = cv2.imread(screenshot_path)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 使用边缘检测 (可以根据设计进一步改进)
edges = cv2.Canny(gray, 50, 150)

# 使用Hough变换找垂直直线，这里假设左侧栏是由垂直的线条或区域分隔的
lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)

# 找到最左侧的第一个直线，一般认为是侧边栏的左侧
left_line_x = float('inf')
for line in lines:
    for rho, theta in line:
        if theta == 0:  # 竖线
            x = abs(rho)
            if x < left_line_x:
                left_line_x = x

# 确认找到的侧边栏位置，这里要根据实际情况调整点击位置
left_sidebar_x = int(left_line_x)

# 暂停一段时间确保页面加载完成
sleep(2)

# 通过selenium模拟点击左侧栏的区域，从上到下逐个点击
height, width, _ = image.shape
click_interval = 50  # 根据实际情况设置点击间距

for y in range(0, height, click_interval):
    try:
        ActionChains(driver).move_by_offset(left_sidebar_x, y).click().perform()
        sleep(2)
        # 这里添加处理点击后的内容，比如爬取、记录或检查结果
        # 例如：
        # result = driver.find_element(By.CSS_SELECTOR, '#result')
        # print(result.text)
        ActionChains(driver).move_by_offset(-left_sidebar_x, -y).perform()  # 将光标移回原点
    except Exception as e:
        print(f"Failed to click at {left_sidebar_x}, {y}: {e}")

# 关闭浏览器
driver.quit()
