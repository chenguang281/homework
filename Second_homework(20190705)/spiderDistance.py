#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests, re

URL = "http://www.bjsubway.com/station/zjgls/"


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
    # page_data = []
    content = re.compile('<div class="line_place".*?<div class="con_text">(.*?)</div>.*?</div>', re.S)
    content_text = re.findall(content, html)
    for i in content_text:
        regular = re.compile('<tr>.*?<th>(.*?)</th>.*?</tr>.*?<td>(.*?)</td>.*?<td>(.*?)</td>', re.S)
        line_data = re.findall(regular, i)
        with open('Data/result.txt', 'a', encoding='utf8') as w:  # 文本追加模式
            for j in line_data:
                w.write("%s-%s\n" % (j[0], j[1]))
            w.close()


if __name__ == '__main__':
    parse_one_page(get_one_page(URL))
