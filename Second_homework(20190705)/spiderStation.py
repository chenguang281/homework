#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests, re

URL = "http://www.bjsubway.com/e/action/ListInfo/?classid=39&ph=1"


# 得到单个网页的信息
def get_one_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        html = response.content
        html_doc = str(html, 'gb2312')
        return html_doc
    return None


# 正则提取表页数据
def parse_one_page(html):
    content = re.compile('<div class="line_place".*?<div class="con_text">.*?<thead>(.*?)</thead>.*?<tbody>(.*?)</tbody>.*?</div>.*?</div>', re.S)
    content_text = re.findall(content, html)
    for i in content_text:
        # print(len(i))

        regular_line = re.compile('<tr.*?<td colspan=.*?>(.*?)</td>.*?</tr>', re.S)
        line_data = re.findall(regular_line, i[0])

        regular_station = re.compile('<tr>.*?<th>(.*?)</th>', re.S)
        station_data = re.findall(regular_station, i[1]) # 站点有漏的，手动补几行。

        with open('Data/result_station.txt', 'a', encoding='utf8') as w:  # 文本追加模式
            w.write(line_data[0]+'\n')
            w.write("->".join(station_data)+"\n")
            w.close()


if __name__ == '__main__':
    parse_one_page(get_one_page(URL))
    # parse_one_page(aaa)