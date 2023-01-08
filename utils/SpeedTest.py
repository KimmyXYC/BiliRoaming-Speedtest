import requests
from multiprocessing import Process, Manager
from utils.Process import loop
from utils.Parameter import get_parameter
from utils.DrawImage import draw_img
import pathlib

USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
VERSION_CODE = get_parameter('version_code')
VERSION_NAME = get_parameter('version_name')


def speedtest(start_time):
    platform = get_parameter('platform')
    session = requests.Session()
    session.headers.update({'user-agent': USER_AGENT})
    session.headers.update({'Build': VERSION_CODE})
    session.headers.update({'x-from-biliroaming': VERSION_NAME})
    session.headers.update({'platform-from-biliroaming': platform})

    mgr = Manager()
    result = mgr.list()

    server_list = mgr.list(read_list())

    p = Process(target=loop, args=(session, result, server_list))
    p.start()
    p.join()

    result = sorted(result, key=lambda r: r['status']['avg'])
    draw_img(result, start_time)


def read_list(file: str = (str(pathlib.Path.cwd()) + "/Config/server.txt")):
    server_list = list()
    with open(file, mode='r', encoding='utf-8') as f:
        for l in f:
            if not l.strip().startswith("#") or l.strip() == "":
                server_list.append(l.strip())
    return server_list
