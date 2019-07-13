#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random


def load_line_data():
    path_dicts = {}
    line_num = 1
    with open('Data/result_station.txt', 'r', encoding='utf8') as r:
        for line in r.readlines():
            line = line.strip('\n')
            if line_num % 2 == 0:
                station_li = line.split('->')
                for k in range(len(station_li)):
                    #     for path_dict in path_dicts.items():
                    #         key , value = path_dict
                    #         if j == key:
                    print(11)
            line_num += 1
    print("over")

    # 广度优先


def breadth_first_search(start, arrive):
    pass


# 深度优先
def depth_first_search(start, arrive):
    pass


if __name__ == '__main__':
    # load_line_data()
    path_dicts = {
        '苹果园': ['1', '2', '3']
    }
    station_li = ['苹果园', '古城', '八角游乐园', '八宝山', '玉泉路', '五棵松', '万寿路', '公主坟', '军事博物馆', '木樨地', '南礼士路', '复兴门', '西单', '天安门西',
                  '天安门东', '王府井', '东单', '建国门', '永安里', '国贸', '大望路', '四惠', '四惠东']
    for k in range(len(station_li)):
        for path_dict in path_dicts.items():
            key, value = path_dict
            if station_li[k] == key:
                value.append(station_li[k])
            else:
                if k == 0:
                    path_dicts[station_li[k]] = station_li[k + 1]
