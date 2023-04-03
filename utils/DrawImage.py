from utils.Parameter import get_parameter

import imgkit
import time


def draw_img(result, duration):
    html_output = '''
    <html>
    <head>
      <style>
        table {
            width: 100%;
        }
        td, th {
            border: 1px solid rgb(190, 190, 190);
            text-align: center;
            padding : 4px;
        }
        td[scope="server"] {
            text-align: left;
        }
        tr:nth-child(even) {
            background-color: #eee;
        }
        tr[scope="header"] > th {
            background-color: #ddd;
        }
        td[scope="ping"] {
            text-align: right;
        }
      </style>
    </head>
    <body>
    <table>
    <center><a>%TITLE%</a></center>
    <caption>%CAPTION%</caption>
    <tr scope="header">
      <th colspan="4">安卓</th>
      <th colspan="3">WEB</th>
      <th rowspan="2">平均</th>
      <th rowspan="2">地址</th>
    </tr>
    <tr scope="header">
      <th>CN</th>
      <th>HK</th>
      <th>TW</th>
      <th>TH</th>
      <th>CN</th>
      <th>HK</th>
      <th>TW</th>
    </tr>
    <tr>
    '''

    html_output = html_output.replace(
        "%CAPTION%", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    html_output = html_output.replace(
        "%TITLE%", get_parameter('output_info', 'title'))

    print('{:^7}|{:^7}|{:^7}|{:^7}| |{:^7}|{:^7}|{:^7}| |{:^7}| {}'.format(
        'cn', 'hk', 'tw', 'th', 'cn', 'hk', 'tw', 'avg', 'server'))

    for r in result:
        text = ''
        for android in r['status']['android']:
            if android['code'] == 0:
                html_output += '<td scope="ping" style="color: {};">{}ms</td>'.format(
                    ping_color(android['ping']), android['ping'])
                text += '{:>5}ms|'.format(android['ping'])
            elif android['code'] == -412 or android['http_code'] == 412:
                html_output += '<td style="color: red;">BAN</td>'
                text += '{:^7}|'.format('BAN')
            elif android['code'] == -10403 or android['http_code'] == 10403:
                html_output += '<td></td>'
                text += '       |'
            else:
                html_output += '<td style="color: red;">{}</td>'.format(
                    android['code'] if android['code'] != -1 else android['http_code'] if android['http_code'] != 404 else '')
                text += '       |'
        text += ' |'
        for web in r['status']['web']:
            if web['code'] == 0:
                html_output += '<td scope="ping" style="color: {};">{}ms</td>'.format(
                    ping_color(web['ping']), web['ping'])
                text += '{:>5}ms|'.format(web['ping'])
            elif web['code'] == -412 or web['http_code'] == 412:
                html_output += '<td style="color: red;">BAN</td>'
                text += '{:^7}|'.format('BAN')
            elif web['code'] == -10403 or web['http_code'] == 10403:
                html_output += '<td></td>'
                text += '       |'
            else:
                html_output += '<td style="color: red;">{}</td>'.format(
                    web['code'] if web['code'] != -1 else web['http_code'] if web['http_code'] != 404 else '')
                text += '       |'
        html_output += '<td scope="ping" style="color: {};">{}ms</td><td scope="server">{}</td></tr>'.format(
            ping_color(r['status']['avg']), r['status']['avg'], r['server'])
        text += ' |{:>5}ms| {}'.format(r['status']['avg'], r['server'])
        print(text)

    html_output += "</table><center><a>测速完成, 共耗时: " + str(duration) + "秒</a></center></body></html>"
    # imgkit.from_string(html_output, get_parameter('output_info', 'file_name'), options={'quiet': ''})
    path_wk = r'D:\Program Files\wkhtmltopdf\bin\wkhtmltoimage.exe'
    config = imgkit.config(wkhtmltoimage=path_wk)
    imgkit.from_string(html_output, 'result.jpg', config=config, options={'quiet': ''})


def ping_color(ping: int) -> str:
    if ping < 150:
        return 'green'
    elif ping < 300:
        return 'orange'
    else:
        return 'red'
