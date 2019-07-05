#!/usr/bin/env python
# -*- coding: utf-8 -*-

# word在文本中出现的次数
def word_frequency(new_file, word):
    with open(new_file, "r") as r:
        line = r.readline()
        while line:
            line_li = line.strip(',').strip('\n').split('-%-%-')
            if len(line_li) > 1 and line_li[0] == word:
                return line_li[1]
            line = r.readline()
    return 0


def word_count(new_file):
    count = 0
    with open(new_file, "r") as r:
        line = r.readline()
        while line:
            line_li = line.strip(',').strip('\n').split('-%-%-')
            if len(line_li) > 1:
                count += int(line_li[1])
            line = r.readline()
    return count


# # 两个词连接起来出现的次数
# def word_frequency(new_file, word):
#     with open(new_file, "r") as r:
#         line = r.readline()
#         while line:
#             line_li = line.strip(',').split('-%-%-')
#             if len(line_li) > 1 and line_li[0] == word:
#                 return line_li[1]
#             line = r.readline()


if __name__ == '__main__':
    aa = word_frequency('word_count.txt', '经济运行')
    print(aa)
