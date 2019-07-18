#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
from sklearn.datasets import load_boston


def price(rm, k, b):
    return k * rm + b


def loss(y, y_hat):
    return sum((y_i - y_hat_i) ** 2 for y_i, y_hat_i in zip(list(y), list(y_hat))) / len(list(y))


def partial_k(x, y, y_hat):
    n = len(y)

    grandient = 0
    for x_i, y_i, y_hat_i in zip(list(x), list(y), list(y_hat)):
        grandient += ((y_i - y_hat_i) * x_i)

    return -2 / n * grandient


def partial_b(x, y, y_hat):
    n = len(y)

    grandient = 0
    for y_i, y_hat_i in zip(list(y), list(y_hat)):
        grandient += (y_i - y_hat_i)
    return -2 / n * grandient


def aa():
    data = load_boston()
    x, y = data['data'], data['target']
    x_rm = x[:, 5]

    trying_times = 2000

    min_loss = float('inf')

    current_k = random.random() * 200 - 100
    current_b = random.random() * 200 - 100

    for i in range(trying_times):

        price_by_k_and_b = [price(r, current_k, current_b) for r in x_rm]

        current_loss = loss(y, price_by_k_and_b)

        if current_loss < min_loss:  # performance became better
            min_loss = current_loss

            print(
                'When time is : {}, get best_k: {} best_b: {}, and the loss is: {}'.format(i, current_k, current_b,
                                                                                           min_loss))

        k_direction = partial_k(x, y, price_by_k_and_b)

        b_direction = partial_b(x, y, price_by_k_and_b)

        current_k = current_k + (-1 * k_direction) * 0.00001
        current_b = current_b + (-1 * b_direction) * 0.00001


if __name__ == '__main__':
    aa()
