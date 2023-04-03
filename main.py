import time
import sys
from loguru import logger
from utils.Parameter import get_config_file, get_parameter
from utils.RefreshKey import refresh_key
from utils.SpeedTest import speedtest
from utils.SftpUpload import upload


def main():
    config = get_config_file()
    expires_date = config['user_info']['expires_date']
    current_timestamp = int(time.time())
    maturity_criteria = 5 * 24 * 60 * 60
    if current_timestamp + maturity_criteria >= expires_date:
        logger.info(f"access_token 已过期，尝试刷新")
        access_token = config['user_info']['access_token']
        refresh_token = config['user_info']['refresh_token']
        appkey = config['platform_info']['appkey']
        appsec = config['platform_info']['appsec']
        refresh_key(access_token, refresh_token, appkey, appsec)
        logger.info("开始测速")
        speedtest()
    else:
        logger.info("开始测速")
        speedtest()
    if get_parameter("sftp", "enable"):
        upload()


if __name__ == '__main__':
    logger.remove()
    handler_id = logger.add(sys.stderr, level="INFO")
    logger.add(sink='run.log',
               format="{time} - {level} - {message}",
               level="INFO",
               rotation="20 MB",
               enqueue=True)
    main()
