#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import read_corpus, load_corpus

# 自己练习，得到一起生成多个句子的方法。
host = """
host = 时间名词 主语名词 形容词 动词 事务名词
时间名词 = 上午、下午、昨天、晌午、半夜、去年、明天
主语名词 = 学生、群众、老头、妇女、同志、叔叔
形容词 = 很快地、迅速地、悄悄地、静静地
动词 = 打、追着、敲着、吆喝、盯着
事务名词 = 蜗牛、猎豹、奥托、棒球、战斗机、冥王星
"""


# host = """
# host = 寒暄 报数 询问 业务相关 结尾
# 报数 = 我是 数字 号 ,
# 数字 = 单个数字 | 数字 单个数字
# 单个数字 = 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
# 寒暄 = 称谓 打招呼 | 打招呼
# 称谓 = 人称 ,
# 人称 = 先生 | 女士 | 小朋友
# 打招呼 = 你好 | 您好
# 询问 = 请问你要 | 您需要
# 业务相关 = 玩玩 具体业务
# 玩玩 = null
# 具体业务 = 喝酒 | 打牌 | 打猎 | 赌博
# 结尾 = 吗？
# """


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
    else:
        li = choice(gram[target])
        sentence = ''  # 最终的句子
        aa = [generate(gram, t) for t in li]
        for s in aa:
            if s is not '/n':
                # if s is not None and s != 'null':
                sentence += s
        return sentence


# 得到句子
def generate_n(n):
    sentences_li = []
    for i in range(n):
        sentences = generate(create_grammar(host, '='), 'host')
        sentences_li.append(sentences)
    return sentences_li


# 得到句子得分
def get_sentences_score(sentences):
    score = 1
    word_li = load_corpus.cut(sentences)
    for i in range(len(word_li)):
        word1 = word_li[i]
        word2 = word_li[i - 1]
        word3 = word2
        if len(word_li) > 1:
            word3 = word_li[i - 2]
        if i == 0:
            score *= word_score(word1)
            continue
        if i == 1:
            score *= word_score(word1, word2)
            continue
        score *= word_score(word1, word2, word3)
    return score


# 统计总词汇数量
def word_score(*args):
    if len(args) == 1:
        numerator = int(read_corpus.word_frequency('word_count.txt', args[0]))
        denominator = int(read_corpus.word_count('word_count.txt'))
    elif len(args) == 2:
        numerator = read_corpus.word_frequency('double_word_count.txt', str(args[1]) + str(args[0]))  # 分子
        denominator = read_corpus.word_frequency('word_count.txt', args[0])  # 分母
    elif len(args) == 3:
        numerator = read_corpus.word_frequency('triple_word_count.txt',
                                               str(args[2]) + str(args[1]) + str(args[0]))  # 分子
        a = str(args[2]) + str(args[1])
        denominator = read_corpus.word_frequency('double_word_count.txt', a)  # 分母
    else:
        return 1 / 80000
    if denominator == 0 or numerator == 0:
        return 1 / 80000
    return int(numerator) / int(denominator)


# 获取列表的第二个元素
def takeSecond(elem):
    return elem[1]


# 得到优质的句子
def generate_best(sentences_li):
    sentences_score_li = []
    for i in sentences_li:
        sentences_score_li.append((i, get_sentences_score(i)))
    sentences_score_li.sort(reverse=True, key=takeSecond)
    return sentences_score_li[0]


if __name__ == '__main__':
    li = generate_best(generate_n(10))
    print(li)
