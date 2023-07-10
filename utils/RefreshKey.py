import requests
import time
from loguru import logger
from utils.Parameter import save_config, appsign

USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'


def refresh_key(access_token, refresh_token, appkey, appsec):
    url = 'https://passport.bilibili.com/x/passport-login/oauth2/refresh_token'
    current_timestamp = int(time.time())
    params = {
        'access_token': access_token,
        'refresh_token': refresh_token,
        "ts": current_timestamp
    }
    params = appsign(params, appkey, appsec)
    headers = {'User-Agent': USER_AGENT}
    response = requests.post(url, params=params, headers=headers)
    info_data = response.json()
    logger.debug(info_data)

    try:
        if info_data['code'] == 0:
            token_info = info_data.get('data').get('token_info')
            access_token = token_info['access_token']
            refresh_token = token_info['refresh_token']
            expires_in = token_info['expires_in']
            save_config("access_token", access_token)
            save_config("refresh_token", refresh_token)
            save_config("expires_date", expires_in + current_timestamp)
            logger.success('access_token 刷新成功')
            logger.debug(f"access_token: {access_token}, refresh_token: {refresh_token}, expires_in: {expires_in}")
        else:
            logger.error(f"发生错误, 错误码: {info_data['code']}, access_token 刷新失败")
    except Exception as e:
        logger.error(f"发生错误: {e}, access_token 刷新失败")
