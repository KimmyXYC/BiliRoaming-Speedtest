import json
import pathlib
import hashlib
import time
import urllib.parse
from loguru import logger


def get_config_file():
    try:
        with open((str(pathlib.Path.cwd()) + "/Config/config.json"), 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
            json_file.close()
        return data
    except Exception as e:
        logger.error(f"获取配置文件失败: {e}")
        return None


def get_parameter(*parameters):
    try:
        value = get_config_file()
        for parameter in parameters:
            value = value.get(parameter)
        return value
    except Exception as e:
        logger.error(f"获取指定参数失败: {e}")
        return None


def save_config(value, parameter):
    try:
        with open((str(pathlib.Path.cwd()) + "/Config/config.json"), 'r+', encoding='utf-8') as json_file:
            data = json.load(json_file)
            data["user_info"][parameter] = value
            json_file.seek(0)
            json.dump(data, json_file, ensure_ascii=False, indent=2)
            json_file.truncate()
            json_file.close()
    except Exception as e:
        logger.error(f"保存配置文件失败: {e}")


def read_server_list(file: str = (str(pathlib.Path.cwd()) + "/Config/server.txt")):
    server_list = list()
    with open(file, mode='r', encoding='utf-8') as f:
        for line in f:
            if not line.strip().startswith("#") or line.strip() == "":
                server_list.append(line.strip())
    return server_list


def appsign(params, appkey, appsec):
    if 'ts' not in params.keys():
        params.update({'ts': int(time.time())})
    params.update({'appkey': appkey})
    params = dict(sorted(params.items()))
    query = urllib.parse.urlencode(params)
    sign = hashlib.md5((query + appsec).encode()).hexdigest()
    params.update({'sign': sign})
    return params
