#!/usr/bin/env python
# -*- coding: utf-8 -*-
import jieba
from collections import Counter


# 切词方法
def cut(string):
    return list(jieba.cut(string))


# 读取训练集，得到每个词
def word_dicts():
    total_dict = []
    for i, line in enumerate((open('new_file.txt'))):
        # if i > 100: break
        total_dict += cut(line)
    return total_dict


# 新文本续写
# 词语-%-%-次数
def write_file(file_name, toup):
    try:
        with open(file_name, "a") as r:
            for k, v in toup.items():
                r.write(k + '-%-%-')
                r.write(str(v))
                r.write('\n')
            r.close()
    except:
        print("-------" + k, v)
    finally:
        r.close()


# 生成单个词语在文本中出现的次数的文件
def word_count():
    word_toup = Counter(word_dicts())
    write_file('word_count.txt', word_toup)


"""
通过2-gram可以知道P(w1, w2, w3, … , wn)=P(w1)P(w2|w1)P(w3|w1w2)P(w4|w1w2w3)…P(wn|w1w2…wn-1)≈P(w1)P(w2|w1)P(w3|w1w2)P(w4|w2w3)…P(wn|wn-2wn-1)
也就是说，我们需要提前准备好，w1的次数统计，在word_count中已经实现了，接下来，我么需要统计，w1w2按照规定顺序出现的次数。也就是说我们需要统计两个连词和三个连词出现的次数，下面我们来看一下我们的方法
"""


# file_name 为要写入的文件名
# n为几个连词，比如要给予两个连词n=2，三个连词n=3
def many_word_count(file_name, n=2):
    li = word_dicts()  # 拿到切词结果
    double_li = []
    # print(len(li))
    for j in range(len(li) - n):
        double_li.append(''.join(li[j:j + n]))
    word_toup = Counter(double_li)
    write_file(file_name, word_toup)


if __name__ == '__main__':
    # word_count()
    # many_word_count('double_word_count.txt', 2)
    many_word_count('triple_word_count.txt', 3)
