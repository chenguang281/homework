#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random


def load_line_data():
    line_num = 1
    path_dicts = {}
    with open('Data/result_station.txt', 'r', encoding='utf8') as r:
        for line in r.readlines():
            line = line.strip('\n')
            if line_num % 2 == 0:
                station_li = line.split('->')
                for k in range(len(station_li)):
                    if k == 0:
                        append_value = station_li[k]
                        set_value = [station_li[k + 1].strip()]
                        for path_dict in path_dicts.items():
                            key, value = path_dict
                            if append_value == key:
                                value.append(station_li[k + 1].strip())
                                set_value = value
                                break
                        path_dicts[station_li[k].strip()] = set_value
                    elif k == len(station_li) - 1:
                        append_value = station_li[k]
                        set_value = [station_li[k - 1].strip()]
                        for path_dict in path_dicts.items():
                            key, value = path_dict
                            if append_value == key:
                                value.append(station_li[k - 1].strip())
                                set_value = value
                                break
                        path_dicts[station_li[k].strip()] = set_value
                    else:
                        append_value = station_li[k]
                        set_value = [station_li[k - 1].strip(), station_li[k + 1].strip()]
                        for path_dict in path_dicts.items():
                            key, value = path_dict
                            if append_value == key:
                                value.append(station_li[k - 1].strip())
                                value.append(station_li[k + 1].strip())
                                set_value = value
                                break
                        path_dicts[station_li[k].strip()] = set_value
            line_num += 1
    return path_dicts


# 广度优先
def breadth_first_search(start, arrive, connrction_grpah):
    # path_dicts = load_line_data()
    pathes = [[start]]
    visitied = set()

    while pathes:
        path = pathes.pop(0)
        froninter = path[-1]

        if froninter in visitied:
            continue
        successors = connrction_grpah[froninter]

        for city in successors:
            new_path = path + [city]
            pathes.append(new_path)

            if city == arrive:
                return new_path
        visitied.add(froninter)


# 深度优先
def depth_first_search(start, arrive):
    pass


if __name__ == '__main__':
    print(breadth_first_search('西直门', '东直门', load_line_data()))
