#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random

# 课堂练习
simple_grammar = """
sentence => noun_phrase verb_phrase
noun_phrase => Article Adj* noun
Adj* => null | Adj Adj*
verb_phrase => verb noun_phrase
Article =>  一个 | 这个
noun =>   女人 |  篮球 | 桌子 | 小猫
verb => 看着   |  坐在 |  听着 | 看见
Adj =>  蓝色的 | 好看的 | 小小的
"""

host = """
host = 寒暄 报数 询问 业务相关 结尾 
报数 = 我是 数字 号 ,
数字 = 单个数字 | 数字 单个数字 
单个数字 = 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 
寒暄 = 称谓 打招呼 | 打招呼
称谓 = 人称 ,
人称 = 先生 | 女士 | 小朋友
打招呼 = 你好 | 您好 
询问 = 请问你要 | 您需要
业务相关 = 玩玩 具体业务
玩玩 = null
具体业务 = 喝酒 | 打牌 | 打猎 | 赌博
结尾 = 吗？
"""


def create_grammar(grammar_str, split='=>', line_split='\n'):
    grammar = {}
    for line in grammar_str.split(line_split):
        if not line.strip():
            continue
        exp, stmt = line.split(split)
        grammar[exp.strip()] = [s.split() for s in stmt.split('|')]
    return grammar


choice = random.choice


def generate(gram, target):
    if target not in gram:
        return target
    return ''.join([e if e != '/n' else '\n' for e in [generate(gram, t) for t in choice(gram[target])] if e != 'null'])


def generate_n(gram, target):
    if target not in gram:
        return target
    return ''.join(
        [e for e in [generate_n(gram, t) for t in choice(gram[target])] if e != 'null'])


if __name__ == '__main__':
    for i in range(10):
        adj = generate(create_grammar(host, '='), target='host')
        print(adj)
