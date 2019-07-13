#!/usr/bin/env python
# -*- coding: utf-8 -*-

simple_connection_info = {
    '北京': ['太原', '沈阳'],
    '太原': ['北京', '西安', '郑州'],
    '兰州': ['西安'],
    '西安': ['兰州', '长沙'],
    '长沙': ['福州', '南宁']
}


def search(city1, city2, connrction_grpah):
    pathes = [[city1]]

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

            if city == city2:
                return new_path
        visitied.add(froninter)


if __name__ == '__main__':
    print(search('兰州', '福州', simple_connection_info))
