#!/usr/bin/env python
# -*- coding: utf-8 -*-
from matplotlib import pyplot as plt

import math
import networkx as nx


def geo_distance(origin, destination):
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371  # km

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) * math.sin(dlat / 2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) * math.sin(dlon / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = radius * c

    return d


def get_geo_distance(city1, city2, city_location):
    return geo_distance(city_location[city1], city_location[city2])


if __name__ == '__main__':
    draw = {

    }
    with open('Data/result_distance.txt', 'r', encoding='utf8') as r:
        for line in r.readlines():
            line_li = line.split('->')
            x, y = line_li[1].strip('\n').split(',')
            draw[line_li[0]] = [float(x)*10000, float(y)*10000]
            r.readline()
    distance = get_geo_distance('苹果园', '复兴门', draw)

    station_graph = nx.Graph()
    station_graph.add_nodes_from(draw.keys())

    nx.draw(station_graph, draw, with_labels=True, node_size=20)
    plt.show()
