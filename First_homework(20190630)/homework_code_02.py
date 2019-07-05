#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random

# 自己练习
host = """
host = 时间名词 主语名词 形容词 动词 事务名词 
时间名词 = 上午、过去、将来、午夜、三更、甲戊、上世纪
主语名词 = 学生、群众、老头、妇女、同志、叔叔
形容词 = 很快地、迅速地、悄悄地、静静地
动词 = 打、追着、敲着、吆喝、盯着
事务名词 = 蜗牛、猎豹、奥托、棒球、战斗机、冥王星
"""


# 该方法主要是将文本转换成字典类型的数据
def create_grammar(grammar_str, split='=', line_split='\n', code_split='、'):
    grammar = {}
    for line in grammar_str.split(line_split):
        if line is '':
            continue
        k, v = line.split(split)
        grammar[k.strip()] = [s.split() for s in v.split(code_split)]
    return grammar


# 随机选择
choice = random.choice


# 得到句子 gram：文本   target：句子模式
def generate(gram, target):
    if target not in gram:
        return target
    return ''.join(
        [e for e in [generate(gram, t) for t in choice(gram[target])] if e != 'null'])


if __name__ == '__main__':
    # create_grammar(host)
    for i in range(10):
        adj = generate(create_grammar(host, '='), target='host')
        print(adj)
