import requests
import time
import json
import hashlib
import urllib.parse

USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'


def refresh_key(access_token, refresh_token, appkey, appsec):
    url = 'https://passport.bilibili.com/x/passport-login/oauth2/refresh_token'
    current_timestamp = int(time.time())
    params = {'access_token': access_token, 'refresh_token': refresh_token,
              "ts": current_timestamp}
    params = appsign(params, appkey, appsec)
    headers = {'User-Agent': USER_AGENT}
    response = requests.post(url, params=params, headers=headers)
    info_data = response.json()
    # print(info_data)
    token_info = info_data.get('data').get('token_info')
    access_token = token_info.get('access_token')
    refresh_token = token_info.get('refresh_token')
    expires_in = token_info.get('expires_in')
    save_key(access_token, refresh_token, expires_in)
    print('access_token刷新成功')
    # print("access_token:", access_token, "refresh_token:", refresh_token, "expires_in:", expires_in)


def appsign(params, appkey, appsec):
    params.update({'appkey': appkey})
    params = dict(sorted(params.items()))
    query = urllib.parse.urlencode(params)
    sign = hashlib.md5((query + appsec).encode()).hexdigest()
    params.update({'sign': sign})
    return params


def save_key(access_token, refresh_token, expires_in):
    current_timestamp = int(time.time())
    expires_date = expires_in + current_timestamp
    with open('config.json', 'r+') as json_file:
        data = json.load(json_file)
        data['access_token'] = access_token
        data['refresh_token'] = refresh_token
        data['expires_date'] = expires_date
        json_file.seek(0)
        json.dump(data, json_file)
        json_file.truncate()
