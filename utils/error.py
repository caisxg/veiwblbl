import sys
import os

# 获取项目根目录的绝对路径
project_root = os.path.dirname(os.path.abspath(__file__))

# 将项目根目录添加到sys.path中
sys.path.append(project_root)

class CookieError(Exception):
    def __init__(self, info):
        self.info = info

    def __str__(self):
        return repr(self.info)


class CaptchaError(Exception):
    def __init__(self, info):
        self.info = info

    def __str__(self):
        return repr(self.info)
