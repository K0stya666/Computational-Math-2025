import numpy as np

# Построение таблицы конечных разностей

def diff_table(xs, ys):
    n = len(xs)
    table = np.zeros((n, n))
    table[:, 0] = ys
    for j in range(1, n):
        for i in range(n-j):
            table[i, j] = (table[i+1, j-1] - table[i, j-1]) / (xs[i+j] - xs[i])
    return table

# Полином Лагранжа

def lagrange(xs, ys, x0):
    n = len(xs)
    result = 0.0
    for i in range(n):
        term = ys[i]
        for j in range(n):
            if j != i:
                term *= (x0 - xs[j]) / (xs[i] - xs[j])
        result += term
    return result

# Полином Ньютона (разделённые разности)

def newton_divided(xs, ys, x0):
    table = diff_table(xs, ys)
    n = len(xs)
    result = table[0, 0]
    prod = 1.0
    for j in range(1, n):
        prod *= (x0 - xs[j-1])
        result += table[0, j] * prod
    return result

# Полином Ньютона на основе конечных разностей (вперёд)

def newton_forward(xs, ys, x0):
    n = len(xs)
    h = xs[1] - xs[0]
    t = (x0 - xs[0]) / h
    table = diff_table(xs, ys)
    result = table[0, 0]
    prod = 1.0
    for i in range(1, n):
        prod *= (t - (i-1)) / i
        result += prod * table[0, i]
    return result

# Полином Ньютона на основе конечных разностей (назад)

def newton_backward(xs, ys, x0):
    n = len(xs)
    h = xs[1] - xs[0]
    t = (x0 - xs[-1]) / h
    table = diff_table(xs, ys)
    result = table[n-1, 0]
    prod = 1.0
    for i in range(1, n):
        prod *= (t + (i-1)) / i
        result += prod * table[n-1-i, i]
    return result