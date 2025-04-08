class SimpsonMethod:
    """
    Класс для численного интегрирования методом Симпсона.
    Порядок точности p = 4.

    В классическом методе Симпсона n берут чётным.
    Если n нечётно — сделаем его (n+1), чтобы правильно
    применить формулу Симпсона.
    """

    def __init__(self):
        self.order = 4

    def integrate(self, f, a, b, n):
        if n % 2 != 0:
            n += 1  # делаем n чётным
        h = (b - a) / n
        s = f(a) + f(b)
        s_odd = 0.0  # сумма f на нечётных узлах
        s_even = 0.0  # сумма f на чётных узлах

        for k in range(1, n):
            xk = a + k * h
            if k % 2 == 0:
                s_even += f(xk)
            else:
                s_odd += f(xk)

        return (s + 2 * s_even + 4 * s_odd) * h / 3.0