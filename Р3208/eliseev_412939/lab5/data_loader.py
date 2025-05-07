import numpy as np

def load_from_keyboard():
    n = int(input("Введите количество точек данных: "))
    xs, ys = [], []
    for i in range(n):
        x = float(input(f"x[{i}]: "))
        y = float(input(f"y[{i}]: "))
        xs.append(x)
        ys.append(y)
    return np.array(xs), np.array(ys)

def load_from_file(filename):
    """
    Загрузка данных из файла: каждая строка содержит два числа x, y, разделённых пробелом.
    """
    data = np.loadtxt(filename)
    xs, ys = data[:, 0], data[:, 1]
    return xs, ys

def load_from_function():
    import math
    funcs = {"sin": math.sin, "cos": math.cos, "exp": math.exp, "x^2": lambda x: x**2}
    print("Доступные функции:")
    for i, (name, _) in enumerate(funcs.items()):
        print(f"{i}: {name}")
    idx = int(input("Выберите индекс функции: "))
    name = list(funcs.keys())[idx]
    f = funcs[name]
    a = float(input("Начало интервала a: "))
    b = float(input("Конец интервала b: "))
    m = int(input("Количество точек (>=2): "))
    xs = np.linspace(a, b, m)
    ys = np.array([f(x) for x in xs])
    return xs, ys