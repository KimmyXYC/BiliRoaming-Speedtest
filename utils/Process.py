import requests
import time
import hashlib
from requests.exceptions import ConnectionError, ReadTimeout
from simplejson.errors import JSONDecodeError
from utils.Parameter import get_parameter
from multiprocessing import Process
from urllib.parse import urlencode

ACCESS_KEY = get_parameter('access_token')
APP_KEY = get_parameter('appkey')
APP_SEC = get_parameter('appsec')
PLATFORM = get_parameter('platform')
APP_KEY_TH = '7d089525d3611b1c'
APP_SEC_TH = 'acd495b248ec528c2eed1e862d393126'

AREA_LIST = [
    {'cn': 266323},
    {'hk': 425578},
    {'tw': 285951},
    {'th': 377544}
]


def processing(server, server_result, session, result):
    try:
        session.head(f'https://{server}', timeout=15)
    except Exception as e:
        # print(e)
        return
    count = 0
    total = 0
    for area_data in AREA_LIST:
        area = list(area_data.keys())[0]
        ep_id = list(area_data.values())[0]

        # print(area)

        test_url = ''
        if area != 'th':
            query: dict = {
                'access_key': ACCESS_KEY,
                'area': area,
                'ep_id': ep_id,
                'fnver': 0,
                'fnval': 464,
                'platform': PLATFORM,
                'fourk': 1,
                'qn': 125
            }
            test_url = 'https://{}/pgc/player/api/playurl?{}'.format(
                server, sign_query(query, APP_KEY, APP_SEC))
        else:
            query: dict = {
                'access_key': ACCESS_KEY,
                'area': area,
                'ep_id': ep_id,
                'fnver': 0,
                'fnval': 464,
                'fourk': 1,
                'platform': PLATFORM,
                'qn': 125,
                's_locale': 'zh_SG'
            }
            test_url = 'https://{}/intl/gateway/v2/ogv/playurl?{}'.format(
                server, sign_query(query, APP_KEY_TH, APP_SEC_TH))
        try:
            time.sleep(1.5)
            session.get(test_url, timeout=10)
            time.sleep(1.5)
            response: requests.Response = session.get(test_url, timeout=10)
            ping = int(response.elapsed.total_seconds() * 1000)
            if not response.ok:
                # print((response.text[:64] + '..') if len(response.text) > 64 else response.text)
                server_result['status']['android'].append(
                    {
                        'area': area,
                        'ping': ping,
                        'http_code': response.status_code,
                        'code': -1,
                    }
                )
                continue
        except ConnectionError as e:
            # print(e)
            server_result['status']['android'].append(
                {
                    'area': area,
                    'ping': -1,
                    'http_code': -1,
                    'code': -1,
                }
            )
            continue
        except ReadTimeout as e:
            # print(e)
            server_result['status']['android'].append(
                {
                    'area': area,
                    'ping': -1,
                    'http_code': -1,
                    'code': -1,
                }
            )
            continue
        try:
            data = response.json()
            if data['code'] == 0:
                count += 1
                total += ping
            # if data['code'] != 0:
            #     print((response.text[:64] + '..') if len(response.text) > 64 else response.text)
            server_result['status']['android'].append(
                {
                    'area': area,
                    'ping': ping,
                    'http_code': response.status_code,
                    'code': data['code'],
                }
            )
        except JSONDecodeError as e:
            if '"code":0,' in response.text:
                count += 1
                total += ping
                server_result['status']['android'].append(
                    {
                        'area': area,
                        'ping': ping,
                        'http_code': response.status_code,
                        'code': 0,
                    }
                )
                continue
            if '"code":-412,' in response.text:
                count += 1
                total += ping
                server_result['status']['android'].append(
                    {
                        'area': area,
                        'ping': ping,
                        'http_code': response.status_code,
                        'code': -412,
                    }
                )
                continue
            # print(e)
            # print(response.headers['content-type'])
            # print((response.text[:64] + '..') if len(response.text) > 64 else response.text)
            server_result['status']['android'].append(
                {
                    'area': area,
                    'ping': ping,
                    'http_code': -1,
                    'code': -1,
                }
            )
            continue

    for area_data in AREA_LIST:
        area = list(area_data.keys())[0]
        ep_id = list(area_data.values())[0]

        # print(area)

        test_url = ''
        if area != 'th':
            query: dict = {
                'access_key': ACCESS_KEY,
                'area': area,
                'ep_id': ep_id,
                'fnver': 0,
                'fnval': 464,
                'platform': PLATFORM,
                'fourk': 1,
                'qn': 125
            }
            test_url = 'https://{}/pgc/player/web/playurl?{}'.format(
                server, sign_query(query, APP_KEY, APP_SEC))
        else:
            continue
        try:
            time.sleep(1.5)
            session.get(test_url, timeout=10)
            time.sleep(1.5)
            response: requests.Response = session.get(test_url, timeout=10)
            ping = int(response.elapsed.total_seconds() * 1000)
            if not response.ok:
                # print((response.text[:64] + '..') if len(response.text) > 64 else response.text)
                server_result['status']['web'].append(
                    {
                        'area': area,
                        'ping': ping,
                        'http_code': response.status_code,
                        'code': -1,
                    }
                )
                continue
        except ConnectionError as e:
            # print(e)
            server_result['status']['web'].append(
                {
                    'area': area,
                    'ping': -1,
                    'http_code': -1,
                    'code': -1,
                }
            )
            continue
        except ReadTimeout as e:
            # print(e)
            server_result['status']['web'].append(
                {
                    'area': area,
                    'ping': -1,
                    'http_code': -1,
                    'code': -1,
                }
            )
            continue
        try:
            data = response.json()
            if data['code'] == 0:
                count += 1
                total += ping
            # if data['code'] != 0:
            #     print((response.text[:64] + '..') if len(response.text) > 64 else response.text)
            server_result['status']['web'].append(
                {
                    'area': area,
                    'ping': ping,
                    'http_code': response.status_code,
                    'code': data['code'],
                }
            )
        except JSONDecodeError as e:
            if '"code":0,' in response.text:
                count += 1
                total += ping
                server_result['status']['web'].append(
                    {
                        'area': area,
                        'ping': ping,
                        'http_code': response.status_code,
                        'code': 0,
                    }
                )
                continue
            if '"code":-412,' in response.text:
                print('412')
                count += 1
                total += ping
                server_result['status']['web'].append(
                    {
                        'area': area,
                        'ping': ping,
                        'http_code': response.status_code,
                        'code': -412,
                    }
                )
                continue
            # print(e)
            # print(response.headers['content-type'])
            # print((response.text[:64] + '..') if len(response.text) > 64 else response.text)
            server_result['status']['web'].append(
                {
                    'area': area,
                    'ping': ping,
                    'http_code': -1,
                    'code': -1,
                }
            )
            continue
    avg = 15000
    if count > 0:
        avg = int(total / count)
    server_result['status']['avg'] = avg
    result.append(server_result)


def loop(session, result, server_list):
    for server in server_list:
        # print()
        # print(server)
        server_result: dict = {
            'server': server,
            'status': {
                'web': [],
                'android': []
            }
        }
        Process(target=processing, args=(
            server, server_result, session, result)).start()


def sign_query(query: dict, appkey: str, appsec: str) -> str:
    return sign_query_time(query, appkey, appsec, int(time.time()))


def sign_query_time(query: dict, appkey: str, appsec: str, ts: int) -> str:
    query['appkey'] = appkey
    query['ts'] = ts
    query = dict(sorted(query.items()))
    query['sign'] = hashlib.md5(
        (urlencode(query) + appsec).encode(encoding='utf-8')).hexdigest()
    return urlencode(query)
