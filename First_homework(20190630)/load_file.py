#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import pandas as pd


def load_file(file_name, new_file, column, coding='utf-8'):
    file = pd.read_csv(file_name, encoding=coding)
    content = file[column].tolist()
    for i in content:
        try:
            if type(i) != str:
                continue
            content_etl = re.findall(r'\w+', i)
            with open(new_file, "a") as r:
                str_content = ''.join(content_etl)
                r.write(str_content)
                r.write('\n')
                r.close()
        except:
            print(i + '报错了，日～！')


if __name__ == '__main__':
    file_name_one = '../Data/movie_comments.csv'
    file_name_two = '../Data/sqlResult_1558435.csv'
    new_file = 'new_file.txt'
    column = 'comment'
    load_file(file_name_one, new_file, column)
