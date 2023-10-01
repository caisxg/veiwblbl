import datetime
import os
import random
import shutil
import sys
import time
from pathlib import Path

from playwright.sync_api import expect, sync_playwright

from pageset import open_browser
from utils.loghelper import loginfo


## 生成截图文件名
def screen_name():
    screen_dir = Path("screenshots", time.strftime("%Y%m%d", time.localtime()))
    if not screen_dir.exists():
        screen_dir.mkdir(parents=True, exist_ok=True)

    now_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
    png_name = Path(screen_dir, f"screnn_{now_time}.png")
    return str(png_name.absolute())


## 按文件名排序,删除最早的文件
def delete_oldest_folders(directory, num_to_keep, reverse_order=False):
    directory_path = Path(directory)

    if not directory_path.exists():
        return

    folders = [f for f in directory_path.iterdir() if f.is_dir()]
    if len(folders) <= num_to_keep:
        return

    folders.sort(key=lambda f: f.name, reverse=reverse_order)
    print(folders)
    num_folders_to_delete = len(folders) - num_to_keep
    for i in range(num_folders_to_delete):
        folder_to_delete = folders[i]
        loginfo(f"删除:{folder_to_delete}")
        shutil.rmtree(folder_to_delete)


if __name__ == "__main__":
    # 获取项目根目录的绝对路径
    try:
        project_root = Path(__file__).parent
    except:
        project_root = Path(os.getcwd())
    # 将项目根目录添加到sys.path中
    sys.path.append(project_root)
    os.chdir(project_root)
    loginfo(f"当前工作目录: {os.getcwd()}")

    try:
        browser_config = {
            "browserkernel": "chromium",
            "channel": "msedge",
            "headless": False,
            "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.57",
            # 用户目录随便写
            "user_data_dir": "~/Default",
        }
        url = "https://live.bilibili.com/30279606"
        time.sleep(random.uniform(2, 5))
        [page, context, pp] = open_browser(url, browser_config)
        page.wait_for_timeout(random.uniform(1000, 4000))
        time.sleep(random.uniform(2, 5))

        current_time = datetime.datetime.now().time()
        loginfo(f"当前时间: {current_time}")

        is_exec = datetime.time(23, 0) <= current_time <= datetime.time(24, 0) or datetime.time(0, 0) <= current_time <= datetime.time(1, 0)
        if not is_exec:
            nn = 1
        else:
            nn = 23
        loginfo(f"循环次数: {nn}")
        for ii in range(nn):  # 这里设置循环次数，你可以根据需要调整次数
            x = random.randint(0, 700)
            y = random.randint(0, 900)
            page.mouse.move(x, y)
            page.keyboard.press("Enter")
            loginfo(f"移动鼠标到: {x}, {y}")
            loginfo(f"当前时间为: {datetime.datetime.now().time()}")
            if ii > 1:
                page.wait_for_timeout(random.randint(1000 * 40 * 0.5, 1000 * 45 * 0.5))  # 随机等待时间，单位是毫秒, 这里是 500秒 到 1500秒之间
            if ii % 10 == 0 or ii <= 10:
                loginfo(f"截图")
                page.screenshot(path=screen_name())

        page.close()
        context.close()
        pp.stop()
    except:
        loginfo(f"发生错误,关闭浏览器")
        page.close()
        context.close()
        pp.stop()
    finally:
        shutil.rmtree("~/Default")
    loginfo(f"尝试清理截图文件夹,防止占用磁盘空间")
    delete_oldest_folders("screenshots", 5)
