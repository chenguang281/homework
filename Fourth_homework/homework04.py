#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gensim.models import word2vec
import re
import jieba
import codecs
import logging
import opencc
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt


def cut_word():
    """切词处理文本"""
    wiki = codecs.open('wiki', 'r', encoding="utf8")
    train = codecs.open('corpus', 'a', encoding="utf8")
    i = 0
    line = wiki.readline()
    cc = opencc.OpenCC('t2s')
    while line:
        ste = re.findall("[\u4e00-\u9fa5]+", line)
        if len(ste):
            line_data = "".join(ste)
            seg_list = jieba.cut(line_data, cut_all=False)
            train.write(cc.convert(" ".join(seg_list)))
            train.write('\n')
        if i % 100 == 0:
            print("切词到第"+str(i)+"行")
        i += 1
        line = wiki.readline()
    wiki.close()
    train.close()


def train_model():
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    sentences = word2vec.LineSentence('corpus')
    model = word2vec.Word2Vec(sentences, sg=0, size=100, window=50, min_count=2, sample=0.001, hs=1,
                              workers=4)

    model.save('train.model')
    print(model['是'])


def tsne_plot(model):
    "Creates and TSNE model and plots it"
    labels = []
    tokens = []
    for word in model.wv.vocab:
        tokens.append(model[word])
        labels.append(word)

    tsne_model = TSNE(perplexity=40, n_components=2, init='pca', n_iter=2500, random_state=23)
    new_values = tsne_model.fit_transform(tokens)
    x = []
    y = []
    for value in new_values:
        x.append(value[0])
        y.append(value[1])

    plt.figure(figsize=(16, 16))
    for i in range(len(x)):
        plt.scatter(x[i], y[i])
        plt.annotate(labels[i],
                     xy=(x[i], y[i]),
                     xytext=(5, 2),
                     textcoords='offset points',
                     ha='right',
                     va='bottom')
    plt.show()


if __name__ == '__main__':
    # cut_word()
    # train_model()
    model = word2vec.Word2Vec.load('train.model')
    y1 = model.similarity("美丽", "丑陋")
    print("相似度为：", y1)

    y4 = model.doesnt_match("书 书籍 教材 很".split())
    print("不合群的词：", y4)

    y2 = model.most_similar(u"游泳", topn=20)  # 20个最相关的
    print("最相关的词有：\n")
    for item in y2:
        print(item[0], item[1])

    # sentences = word2vec.LineSentence('test')
    # model = word2vec.Word2Vec(sentences, sg=0, size=100, window=20, min_count=2, sample=0.001, hs=1,
    #                           workers=4)
    # tsne_plot(model)
