import time
import random
import sys
from pathlib import Path
from platform import platform, system
from playwright.sync_api import sync_playwright, expect
from utils.tools import create_directory_or_file 
from utils.loghelper import loginfo
import copy
import sys
import os

# 获取项目根目录的绝对路径
try:
    project_root = Path(__file__).parent
except:
    project_root = Path(os.getcwd())
# 将项目根目录添加到sys.path中
sys.path.append(project_root)




def launch_browser(browser_config):
    """
    发射浏览器
    :param browser_config: 浏览器配置
    """
    if not isinstance(browser_config, dict):
        raise TypeError("Invalid browser config data.")
    
    loginfo("加载浏览器配置......")
    # 启动浏览器, 不同浏览器的内核不同, 所以需要分别启动
    # 1. 启动chromium内核的浏览器: 包括chrome, edge, chromium
    # 2. 启动firefox内核的浏览器: 包括firefox
    # 3. 启动webkit内核的浏览器: 包括safari
    try:
        browserkernel = browser_config.get("browserkernel", "chromium")
        loginfo(f"当前浏览器内核为: {browserkernel}")

        common_args = {
            "viewport": {"width": 1440, "height": 900},
            "screen": {"width": 1440, "height": 900},
            "no_viewport": True,
            "bypass_csp": True,
            "color_scheme": "dark",  # light, dark
            "accept_downloads": True
        }
        pp = sync_playwright().start()
        if browserkernel == "chromium":
            ignore_default_args = ["--enable-automation", "--no-sandbox"]
        else:
            ignore_default_args = []

        new_browser_config = copy.deepcopy(browser_config)
        del new_browser_config["browserkernel"]

        current_system = system()
        if current_system == "Linux":
            new_browser_config['headless'] = True

        context = getattr(pp, browserkernel).launch_persistent_context(
            **common_args,
            **new_browser_config,
            ignore_default_args=ignore_default_args
        )
        page = context.pages[0]
        loginfo("浏览器加载完成......")
        return [page, context, pp]
    except:
        # 测试环境下, 为了方便调试, 可以使用下面的代码
        # pp = sync_playwright().start()
        # browser = pp.chromium.launch(headless=True)
        # context = browser.new_context()
        # page = context.new_page()
        # return [page, context, pp]
        raise Exception("浏览器启动失败, 请检查浏览器配置是否正确")
    


def open_browser_with_url(page, url):
    # 打开网页
    loginfo(f"正在打开网页: {url}")
    page.wait_for_timeout(random.uniform(1000, 4000))
    page.goto(url)
    page.wait_for_timeout(random.uniform(1000, 4000))
    assert url in page.url

    myuser_agent = page.evaluate("() => navigator.userAgent")
    loginfo(f"当前使用的 user_agent 为: {myuser_agent}")
    loginfo(f"成功打开网页: {page.url}")
    return page

def open_browser(url, browser_config):
    [page, context, pp] = launch_browser(browser_config)
    page = open_browser_with_url(page, url)
    return [page, context, pp]


__all__ = ["launch_browser", "open_browser_with_url", 'open_browser']

if __name__ == "__main__":
    #loginfo(browser_config)
    browser_config =  {
            "browserkernel": "chromium",
            "channel": "msedge",
            "headless": False,
            "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.57",
             # 用户目录随便写
            "user_data_dir": "/Users/zsc/Library/Application Support/Microsoft Edge/Default2"
        }
    url = "https://www.baidu.com/"
    time.sleep(random.uniform(2, 5))
    [page, context, pp] = open_browser(url, browser_config)
    page.wait_for_timeout(random.uniform(1000, 4000))
    time.sleep(random.uniform(2, 5))
    #print(page.content())
    context.close()
    pp.stop()
    time.sleep(random.uniform(2, 5))
    # 睡眠
        