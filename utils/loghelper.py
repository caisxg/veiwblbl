

import logging
from pathlib import Path
import os

from datetime import datetime
import sys
import os
import time

# 获取项目根目录的绝对路径
project_root = os.path.dirname(os.path.abspath(__file__))

# 将项目根目录添加到sys.path中
sys.path.append(project_root)

# 日志类
class MyLogger:
    def __init__(self, log_file=None, level=logging.INFO, consoleinfo = True):
        self.log_file = log_file
        self.level = level
        self.consoleinfo = consoleinfo
        self.logger = self._create_logger()
    def _create_logger(self):
        logger = logging.getLogger(self.log_file) # 创建一个logger
        logger.setLevel(self.level) # 设置日志等级

        # 创建格式器,表示日志的输出格式
        #formatter = logging.Formatter('%(asctime)s %(levelname)-8s : %(message)s', '%Y-%m-%d %H:%M:%S')
        formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s', '%Y-%m-%d %H:%M:%S')
        # 创建文件处理器，输出到文件
        if self.log_file:
            file_handler = logging.FileHandler(self.log_file, mode='a', encoding='utf-8')
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler) # 将处理器添加到logger中
        if self.consoleinfo:
            # 创建控制台处理器，输出到控制台, 如果只要一种,则注释即可
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)# 将处理器添加到logger中

        return logger

    def log(self, message, level=logging.INFO):
        if level == logging.INFO:
            self.logger.info(message)
        elif level == logging.WARNING:
            self.logger.warning(message)
        elif level == logging.ERROR:
            self.logger.error(message)
        elif level == logging.DEBUG:
            self.logger.debug(message)
        elif level == logging.exception:
            self.logger.exception(message)
        else:
            self.logger.critical(message)

log_dir = Path('logs')
if not log_dir.exists():
    # 如果日志目录不存在,则创建,递归创建
    log_dir.mkdir(parents=True,exist_ok=True)

file_path = Path('mylog.log')

if file_path.exists():
    #created_time = file_path.stat().st_ctime # 获取文件创建时间,在 linux 上没有首次创建时间,只有最后修改时间
    now = datetime.now().timestamp()
    file_size = file_path.stat().st_size / (1024 * 1024)  # 获取文件大小, 单位是 MB
    if file_size > 10:
        # 如果文件大小超过10M,则删除
        #print(f"该日志文件, 大小超过10M, 删除 {file_path}")
        file_path_old = Path(log_dir, f"mylog_{datetime.fromtimestamp(now).strftime('%Y%m%d')}.log")
        print(f"该日志文件, 大小超过10M, 把以前的先打包存储到 {file_path_old}, 然后重新创建新的日志文件,")
        os.rename(file_path, file_path_old)
    # if now - created_time > 60 * 60 * 24:
    #     # 如果文件创建时间超过1天,则删除
    #     file_path_old = Path(log_dir, f"mylog_{datetime.fromtimestamp(created_time).strftime('%Y%m%d')}.log")
    #     print(f"该日志文件, 创建时间超过7天, 把以前的先打包存储到 {file_path_old}, 然后重新创建新的日志文件,")
    #     os.rename(file_path, file_path_old)
    

mylogger = MyLogger(str(file_path))
def loginfo(message):
    mylogger.log(message, level=logging.INFO)
def logwarning(message):
    mylogger.log(message, level=logging.WARNING)
def logerror(message):
    mylogger.log(message, level=logging.ERROR)
def logdebug(message):
    mylogger.log(message, level=logging.DEBUG)
def logexception(message):
    mylogger.log(message, level=logging.exception)
def logcritical(message):
    mylogger.log(message, level=logging.critical)

__all__ = ['MyLogger', 'loginfo', 'logwarning', 'logerror', 'logdebug', 'logexception', 'logcritical']

if __name__ == '__main__':
    # 示例用法
    log_file = 'mylog.log'
    mylogger = MyLogger()

    mylogger.log('This is an info message', level=logging.INFO)
    mylogger.log('This is a warning message', level=logging.WARNING)
    mylogger.log('This is an error message', level=logging.ERROR)
