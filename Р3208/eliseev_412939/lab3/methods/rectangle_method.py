class RectangleMethod:
    """
    Класс для численного интегрирования методом прямоугольников.
    Поддерживает три режима:
      mode='left'   — левые прямоугольники
      mode='right'  — правые прямоугольники
      mode='middle' — средние прямоугольники
    Порядок точности:
      left/right  => p = 1,
      middle      => p = 2
    """

    def __init__(self, mode='left'):
        if mode not in ('left', 'right', 'middle'):
            raise ValueError("mode должен быть 'left', 'right' или 'middle'")
        self.mode = mode
        # Установим порядок точности p
        if self.mode in ('left', 'right'):
            self.order = 1
        else:  # mode == 'middle'
            self.order = 2

    def integrate(self, f, a, b, n):
        """
        Вычисление интеграла от a до b методом прямоугольников,
        с учётом выбранного режима (left / right / middle).
        """
        h = (b - a) / n
        s = 0.0
        if self.mode == 'left':
            x = a
            for _ in range(n):
                s += f(x)
                x += h
        elif self.mode == 'right':
            x = a + h
            for _ in range(n):
                s += f(x)
                x += h
        else:  # 'middle'
            x = a
            for _ in range(n):
                mid = x + h / 2
                s += f(mid)
                x += h

        return s * h