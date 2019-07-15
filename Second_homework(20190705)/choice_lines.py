#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
                        set_value = [station_li[k + 1]]
                        for path_dict in path_dicts.items():
                            key, value = path_dict
                            if append_value == key:
                                value.append(station_li[k + 1])
                                set_value = value
                                break
                        path_dicts[station_li[k]] = set_value
                    elif k == len(station_li) - 1:
                        append_value = station_li[k]
                        set_value = [station_li[k - 1]]
                        for path_dict in path_dicts.items():
                            key, value = path_dict
                            if append_value == key:
                                value.append(station_li[k - 1])
                                set_value = value
                                break
                        path_dicts[station_li[k]] = set_value
                    else:
                        append_value = station_li[k]
                        set_value = [station_li[k - 1], station_li[k + 1]]
                        for path_dict in path_dicts.items():
                            key, value = path_dict
                            if append_value == key:
                                value.append(station_li[k - 1])
                                value.append(station_li[k + 1])
                                set_value = value
                                break
                        path_dicts[station_li[k]] = set_value
            line_num += 1
    return path_dicts


# 广度优先
def breadth_first_search(start, arrive, connrction_grpah):
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
def depth_first_search(start, arrive, connrction_grpah):
    pathes = [[start]]
    visitied = set()

    while pathes:
        path = pathes.pop(0)
        froninter = path[-1]

        if froninter in visitied:
            continue
        successors = connrction_grpah[froninter]

        for city in successors:
            if city in path:
                continue
            new_path = path + [city]
            pathes.append(new_path)

            if city == arrive:
                return new_path
        visitied.add(froninter)
        pathes = sorted(pathes, key=len, reverse=True)


if __name__ == '__main__':
    print(breadth_first_search('上地', '清华东路西口', load_line_data()))
    print(depth_first_search('上地', '清华东路西口', load_line_data()))
