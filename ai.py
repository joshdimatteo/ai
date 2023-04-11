import numpy as np


def linear(n):
    return 4 * n


def relu(n):
    if n > 0:
        return n
    return 0


def l_relu(n):
    if n > 0:
        return n
    return 0.01 * n


def p_relu(a, n):
    if n > 0:
        return n
    return a * n
