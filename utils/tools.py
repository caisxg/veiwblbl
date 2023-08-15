import random
# from faker import Faker #这个不是很好用, 他和其他的库有一定冲突
from lorem_text import lorem
import json
import json5
import yaml
import sys
import os

# 获取项目根目录的绝对路径
project_root = os.path.dirname(os.path.abspath(__file__))

# 将项目根目录添加到sys.path中
sys.path.append(project_root)

from pathlib import Path
from utils.loghelper import loginfo
from datetime import datetime
import requests

def from_response_get_json(response):
    """
    从响应中获取json
    """
    if response.status_code > 200:
        loginfo(f"请求失败, 响应码: {response.status_code}")
        return None

    try:
        return response.json()
    except:
        # 尝试从响应中获取文本
        try:
            text = response.text
            start = text.find("{")
            end = text.rfind("}") + 1  # 从右边开始查找,找到第一个"}"的位置,然后加1

            if start == -1 or end == 0 or start >= end:
                raise ValueError("无法找到有效的JSON字符串")

            json_str = text[start:end]
            json_data = json.loads(json_str)
            return json_data
        except:
            loginfo(f"无法从响应中获取JSON")
            return None

def calculate_days_difference(given_date):
    # 获取当前日期
    current_date = datetime.now().date()

    # 将给定日期转换为datetime对象
    given_date_obj = datetime.strptime(given_date, '%Y-%m-%d').date()

    # 计算天数差异
    days_difference = (current_date - given_date_obj).days

    return days_difference

def calculate_time_difference(start_time, end_time):
    # 假设输入的时间格式为"HH:MM:SS"，例如"12:34:56"
    start_time = datetime.strptime(start_time, "%H:%M:%S")
    end_time = datetime.strptime(end_time, "%H:%M:%S")

    # 设置一个相同的日期部分，例如今天的日期
    today = datetime.now().date()
    start_datetime = datetime.combine(today, start_time.time())
    end_datetime = datetime.combine(today, end_time.time())

    # 计算时间差
    time_difference =  start_datetime - end_datetime

    # 返回时间差，可以根据需要获取总秒数或其他时间单位
    return time_difference.total_seconds()



def check_dict_keys(dictionary, keys):
    if not isinstance(dictionary, dict):
        dictionary = {}
    dict_keys = set(dictionary.keys())

    if keys is None:
        loginfo("没有提供键值列表或字典")
        return False
    
    if isinstance(keys, list):
        task_keys = set(keys)
    elif isinstance(keys, dict):
        task_keys = set(keys.keys())
    else:
        return False
    missing_keys = task_keys - dict_keys
    if missing_keys:
        loginfo(f"字典缺少以下指定的键: {missing_keys}")
        return False
    return True



def read_yaml_file(file_path, **kw):
    """
    读取YAML文件并转换为字典, 返回字典
    """ 
    if isinstance(file_path, str):
        file_path = Path(file_path)

    if not Path(file_path).exists():
        raise Exception(f'文件{file_path}不存在')
    
    with open(file_path, 'r', encoding="utf-8") as f:
        data = yaml.safe_load(f, **kw)
    return data



def write_dict_to_yaml(filename, data, **kw):
    """
    将字典写入yaml文件
    :param filename: 文件名
    :param data: 字典
    :param indent: 缩进
    :param sort_keys: 是否按键排序
    """
    if not isinstance(data, dict):
        raise Exception('data must be dict')
    
    if Path(filename).exists():
        Path(filename).unlink()
    with open(filename, "w", encoding="utf-8") as file:
        yaml.dump(data, file, allow_unicode=True, 
                  sort_keys=False, indent=2, default_flow_style=False, width=3000, **kw)
    

def read_json5_file(file_path, **kw):
    """
    读取JSON5文件并转换为字典, 返回字典, json5文件中的注释会被忽略,普通的 json 文件也可以读取
    """        
    if not Path(file_path).exists():
        raise Exception(f'文件{file_path}不存在')
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json5.load(f, **kw)
    return data

def read_json_file(file_path, **kw):
    """
    读取JSON文件并转换为字典, 返回字典
    """
    if not Path(file_path).exists():
        raise Exception(f'文件{file_path}不存在')
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f, **kw)
    return data

def write_dict_to_json(filename, data, **kw):
    """
    将字典写入json文件
    :param filename: 文件名
    :param data: 字典
    :param indent: 缩进
    :param sort_keys: 是否按键排序
    """
    if not isinstance(data, dict):
        raise Exception('data must be dict')
    
    with open(filename, 'w', encoding="utf-8") as file:
        json.dump(data, file, **kw)


def generate_list_text(num, max_nb_chars = 20):
    words = 10
    result = ['66666666', '主播真厉害', '爱了，爱了', '关注走一走, 活到99',
                           '牛逼！！！', '秀儿，是你吗？', '223333']
    for _ in range(num):
       tmptext = lorem.words(words)
       if len(tmptext) >= max_nb_chars:
           result.append(tmptext[0:max_nb_chars-1])
    selected = random.sample(result, num)
    return selected



# def generate_list_text(num, max_nb_chars = 20):
#     """
#     随机生成一些中/英文文本, 返回一个列表, 列表长度为 num,且列表中的每个元素是字符串且不超过max_nb_chars个字符
#     :param num: 列表长度
#     :param max_nb_chars: 每个元素的最大字符数
#     """
#     # if not isinstance(num, int) or not isinstance(max_nb_chars, int):
#     #     raise Exception('num and max_nb_chars must be int')
#     # n = 8
#     # if max_nb_chars < n:
#     #     raise Exception(f'max_nb_chars must be greater than {n}')
    
#     # result = ['66666666', '主播真厉害', '爱了，爱了', '关注走一走，活到99',
#     #              '牛逼！！！', '秀儿，是你吗？', '223333']
    
#     # for _ in range(num):
#     #     lang = random.choice(['zh_CN', 'en_US'])
#     #     fake = Faker(locale=lang)
#     #     nb = random.randint(n, max_nb_chars)
#     #     text = fake.text(max_nb_chars=nb)
#     #     if len(text) < max_nb_chars:
#     #         result.append(text)
#     #     else:
#     #         result.append(text[:nb])

#     # # 直接从结果中随机取出 num 个元素
#     result = ['66666666', '主播真厉害', '爱了，爱了', '关注走一走，活到99',
#             '牛逼！！！', '秀儿，是你吗？', '223333']
#     selected = random.sample(result, num)
#     return selected



def filter_dict_by_keys(cookies_dict, keys):
    """
    从cookies_dict中过滤出keys中的键, 并返回一个新的字典
    :param cookies_dict: cookies字典
    :param keys: 键列表
    返回值: (cookies_dict2, is_all_founded), cookies_dict2是过滤后的字典, is_all_founded是一个布尔值, 表示是否所有的键都找到了
    """
    cookies_dict2 = {}
    not_found_count = 0
    for key in keys:
        value = cookies_dict.get(key, None)
        if value is not None:
            cookies_dict2[key] = value
        else:
            loginfo(f"cookie 中没找到键: {key}")
            not_found_count += 1    
    if not_found_count > 0:
        loginfo(f"cookie 中某些键没找到的个数: {not_found_count}")
        is_all_founded = 0 
    else:
        loginfo("cookie 中的键都找到了")
        is_all_founded = 1
    
    return cookies_dict2, is_all_founded



def convert_cookie_str_to_dict(cookie_str):
    """
    将cookie字符串转换为字典
    :param cookie_str: cookie字符串
    :return: 转换后的cookie字典
    """
    if not cookie_str:
        return {}  # 处理空字符串或空值的情况，返回空字典

    cookie_list = cookie_str.split(';')
    cookie_dict = {}
    for item in cookie_list:
        try:
            key, value = item.strip().split('=', 1)  # 处理键值对格式错误的情况
            cookie_dict[key] = value
        except ValueError:
            # 如果键值对格式错误，则跳过该键值对或根据需求处理异常情况
            pass

    return cookie_dict


def convert_cookie_dict_to_str(cookie_dict):
    """
    将cookie字典转换为字符串
    :param cookie_dict: cookie字典
    """
    cookie_str = ""
    for key, value in cookie_dict.items():
        cookie_str += f"{key}={value}; "
    cookie_str = cookie_str.rstrip("; ")
    return cookie_str


def create_directory_or_file(path):
    """
    根据路径,创建目录或文件,  如果路径是目录，则递归创建该目录及其子目录, 如果路径是文件，则创建该文件及其父目录,并创建一个空文件
    由于 path.is_file(), 当路径不存在时也会返回fasle,所以这里不用这个方法,这里采用后缀是否为空来判断是否是文件
    :param path: 路径
    """
    if isinstance(path, str):
        path = Path(path) # 如果文件已经存在，则直接返回
        
    if not isinstance(path, Path):
        raise Exception("path 必须是字符串或Path对象")
    
    if path.exists():
        return
    
    if path.suffix != "":
        # 表明是一个文件
        dir_path = path.parent # 获取父目录,
        dir_path.mkdir(mode=0o777, parents=True, exist_ok=True) # 递归创建父目录
        path.touch() # 创建空文件
        return
    else:
        path.mkdir(mode=0o777, parents=True, exist_ok=True) # 表明是一个目录,则递归创建该目录及其子目录,如果目录已经存在,则不会抛出异常
        return


def convert_path_values_to_string(data):
    """
    将字典或列表中的Path对象转换为字符串, 方便写入json文件(主要是为了确定类型,不要矛盾)
    :param data: 字典或列表
    """
    if isinstance(data, dict):
        for key, value in data.items():
            data[key] = convert_path_values_to_string(value)
    elif isinstance(data, list):
        for i, item in enumerate(data):
            data[i] = convert_path_values_to_string(item)
    elif isinstance(data, Path):
        data = str(data)
    return data














def recursive_json_loads(data):
    """
    递归处理字典中的字符串值, 将其转换为字典或列表
    :param data: 字典
    """
    if isinstance(data, dict):
        for kay, value in data.items():
            if isinstance(value, str):
                try:
                    parsed_value = json.loads(value)
                    if isinstance(parsed_value, (dict, list)):
                        data[kay] = parsed_value
                        recursive_json_loads(data[kay])  # 递归处理新的值
                except:
                    pass
            elif isinstance(value, dict):
                recursive_json_loads(value)






def extract_name_value_pairs(data):
    mydict = {}

    def extract_fields_recursive(item):
        if isinstance(item, dict):
            name = item.get('name', None)
            value = item.get('value', None)
            if name is not None and value is not None:
                mydict[name] = value
            for value in item.values():
                extract_fields_recursive(value)
        elif isinstance(item, list):
            for element in item:
                extract_fields_recursive(element)

    extract_fields_recursive(data)
    return mydict




def handdle_storagejson_recursive(file_path):
    """
    该文件来自 PlayWright 存储的 storagejson.json 文件, 该文件中的键名和键值都是字符串, 该函数将其转换为字典
    """
    if not Path(file_path).exists():
        raise Exception(f"文件不存在: {file_path}")
    
    data = read_json_file(file_path)

    # 提取 name 和 value 字段的值，并以字典形式返回
    name_value_dict = extract_name_value_pairs(data)



    # 递归处理 JSON 数据
    recursive_json_loads(name_value_dict)

    return name_value_dict


if __name__ == "__main__":
    
    file_path =  Path("ustatic/u19196/storage_state.json")  # 请替换为实际的 JSON 文件路径
    mm = handdle_storagejson_recursive(file_path=file_path)
    print(mm['liveWatchTracker'])

