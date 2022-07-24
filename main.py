import time
from selenium import webdriver
import xlsxwriter
import re
import os

keyword = input('请输入搜索的关键词：')
keyword = str(keyword)
page = input('请输入要记录的页数：')
page = int(page)
links = []
#os.system('cls')
def broswer(cfg,url,page):
    if cfg == 'headless':
        # 无边框模式
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        #屏蔽JS提示
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(options=options)
    else:
        #有边框模式
        #屏蔽JS提示
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome()
    driver.maximize_window()
    # 隐性等待最长时间
    driver.implicitly_wait(6)
    # 打开网页
    driver.get(url)
    # 接下来是全屏的关键，用js获取页面的宽高，如果有其他需要用js的部分也可以用这个方法
    width = driver.execute_script("return document.documentElement.scrollWidth")
    height = driver.execute_script("return document.documentElement.scrollHeight")
    # 将浏览器的宽高设置成刚刚获取的宽高
    driver.set_window_size(width, height)
    # 检测是否遇到安全验证
    cur_url = driver.current_url
    # 没有安全验证，返回 -1
    safe = cur_url.find('wappass.baidu.com')
    if safe != -1:
        # 出现了安全验证，先关闭原来的窗口
        driver.quit()
        # 本次操作失败
        print("遇到安全验证，正在重试")
        time.sleep(1)
        return -1
    else:
        # 一切正常，打印照片
        # 保存的文件名
        filename = '.\\' + keyword + str(page) + '.png'
        # 获取图片路径列表
        im_path_list.append(filename)
        # 打印照片
        driver.get_screenshot_as_file(filename)
        print("正在打印第%d页" % page)
        global num
        num = int(num) + 1
        driver.quit()
        time.sleep(1)
        return 1

# url 页码计算， 存放到links列表中
for i in range(page):
    p = i * 10
    p = str(p)
    links.append('https://www.baidu.com/s?wd=' + keyword + '&pn=' + p)

# 页码打印计数器
num = 1
# 图片存放路径列表
im_path_list = []

for i in links:
    while True:
        # 启动截图函数
        info = broswer('headless',i,num)
        if info != -1:
            # 程序正常
            break

    time.sleep(1)

# 获取excel文件名字
excel_path = keyword + '.xlsx'
# 打开excel
work = xlsxwriter.Workbook(excel_path)
print("正在保存到excel中")
# 每页的内容都放一个sheet， 以页码标记
for i in range(page):
    sheet = work.add_worksheet(str(i + 1))
    sheet.insert_image('A1', im_path_list[i])
# 关闭excel
work.close()

# 清理图片
for i in im_path_list:
    os.remove(i)

print("图片垃圾清扫完毕")
time.sleep(1)
print("八荒截图器已经工作完毕，5秒后自动退出")
time.sleep(5)
