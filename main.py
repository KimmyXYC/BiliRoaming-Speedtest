import json
import time
from utils.RefreshKey import refresh_key
from utils.SpeedTest import speedtest


def main():
    with open('Config/config.json', 'r') as f:
        config = json.load(f)
    expires_date = config['expires_date']
    current_timestamp = int(time.time())
    maturity_criteria = 5*24*60*60
    if current_timestamp + maturity_criteria >= expires_date:
        print('access_token已过期，尝试刷新')
        access_token = config['access_token']
        refresh_token = config['refresh_token']
        appkey = config['appkey']
        appsec = config['appsec']
        refresh_key(access_token, refresh_token, appkey, appsec)
        speedtest(start_time)
    else:
        speedtest(start_time)


if __name__ == '__main__':
    start_time = time.time()
    main()
    duration = time.time() - start_time
    print(f'测试完成，共耗时 {int(duration)} 秒')
