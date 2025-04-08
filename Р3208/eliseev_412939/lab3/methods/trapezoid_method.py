class TrapezoidMethod:
    """
    Класс для численного интегрирования методом трапеций.
    Порядок точности p = 2.
    """

    def __init__(self):
        self.order = 2

    def integrate(self, f, a, b, n):
        h = (b - a) / n
        s = 0.5 * (f(a) + f(b))  # полусумма значений на краях
        x = a + h
        for _ in range(n - 1):
            s += f(x)
            x += h
        return s * h