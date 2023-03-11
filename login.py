import requests, time, urllib, hashlib, json


class config:
    cid = 86  # 国际电话区号
    appkey = "783bbb7264451d82"
    appsec = "2653583c8873dea268ab9386918b1d65"
    header = {
        "Host": "passport.bilibili.com",
        "buvid": "XU4B4E44813CCE878BC2D965745433AB55B06",
        "env": "prod",
        "app-key": "android64",
        "user-agent":
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
        "x-bili-trace-id":
        "7a709e7790e6e76a7de8c8e48c640c77:7de8c8e48c640c77:0:0",
        "content-type": "application/x-www-form-urlencoded; charset=utf-8",
        # "accept-encoding": "gzip, deflate, br"
    }


def appsign(params, appkey, appsec):
    params.update({'appkey': appkey})
    params = dict(sorted(params.items()))
    query = urllib.parse.urlencode(params)
    sign = hashlib.md5((query + appsec).encode()).hexdigest()
    params.update({'sign': sign})
    return params


def sms_send(phone):
    url = "https://passport.bilibili.com/x/passport-login/sms/send"
    data = {"cid": config.cid, "tel": phone, "ts": int(time.time())}
    data = appsign(params=data, appkey=config.appkey, appsec=config.appsec)
    r = requests.post(url=url, data=data, headers=config.header)
    return r.json()["code"], r.json()["message"], r.json(
    )["data"]["captcha_key"]


def sms_login(captcha_key, code, phone):
    url = "https://passport.bilibili.com/x/passport-login/login/sms"
    data = {
        "captcha_key": captcha_key,
        "cid": config.cid,
        "code": code,
        "tel": phone,
        "ts": int(time.time())
    }
    data = appsign(params=data, appkey=config.appkey, appsec=config.appsec)
    r = requests.post(url=url, data=data, headers=config.header)
    return r.json()


def update_info():
    with open("login_info.json", "r", encoding="utf-8") as r:
        token_info = json.load(r)["data"]["token_info"]
    access_token, refresh_token, expires_in = token_info[
        "access_token"], token_info["refresh_token"], token_info["expires_in"]
    current_timestamp = int(time.time())
    expires_date = expires_in + current_timestamp
    with open('Config/config.json', 'r+', encoding='utf-8') as json_file:
        data = json.load(json_file)
        data['access_token'] = access_token
        data['refresh_token'] = refresh_token
        data['expires_date'] = expires_date
        data['appkey'] = config.appkey
        data['appsec'] = config.appsec
        json_file.seek(0)
        json.dump(data, json_file, ensure_ascii=False, indent=2)
        json_file.truncate()


if __name__ == "__main__":
    phone = input("请输入手机号:")
    status_code, msg, captcha_key = sms_send(phone=phone)
    if msg != "0": print(msg)
    if status_code != 0: exit()
    code = input("请输入验证码:")
    login_info = sms_login(captcha_key=captcha_key, code=code, phone=phone)
    with open('login_info.json', 'w', encoding='utf-8') as w:
        json.dump(login_info, w, ensure_ascii=False, indent=2)
    print(login_info["data"]["message"])
    if login_info["data"]["status"] == 0:
        print("登录成功!")
        update_info()
    else:
        print("登录失败...")
