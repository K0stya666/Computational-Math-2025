import numpy as np
from dto.equation import Equation
from dto.result import Result
from methods.method import MAX_ITERATIONS


def create_jacobian(x, y, system, h=1e-6):
    """
    Строит якобиан для системы из двух уравнений
    :param x, y: начальные приближения
    :param system: система уравнений
    :param h: шаг для численного дифференцирования (по умолчанию 1e-6)
    :return: якобиан 2x2
    """
    f = system[0].function
    g = system[1].function

    # частные производные по x, y для функции f(x, y)
    fx_ = (f(x + h, y) - f(x, y)) / h
    fy_ = (f(x, y + h) - f(x, y)) / h

    # частные производные по x, y для функции g(x, y)
    gx_ = (g(x + h, y) - g(x, y)) / h
    gy_ = (g(x, y + h) - g(x, y)) / h

    jac = [
        [fx_, fy_],
        [gx_, gy_],
    ]

    return jac

class NewtonMethod:
    """
    Класс для реализации метода Ньютона
    """
    name = "Метод Ньютона"

    def __init__(self, system: list[Equation], x0: float, y0: float,  eps: float):
        self.system = system
        self.x0 = x0
        self.y0 = y0
        self.eps = eps


    def solve(self) -> Result:
        """
        Метод Ньютона:
        функция f(x) на отрезке [a, b] заменяется касательной и в качестве приближённого значения корня
        принимается точка пересечения касательной с осью абсцисс.
        :return:
        """
        system = self.system
        v = [self.x0, self.y0]  # Текущая точка (вектор)
        eps = self.eps
        iteration = 0


        while True:
            if iteration >= MAX_ITERATIONS:
                raise Exception(f'Выполнено {MAX_ITERATIONS} итераций. Решение не найдено.')
            iteration += 1

            jac = create_jacobian(v[0], v[1], system)

            f = system[0].function(v[0], v[1])
            g = system[1].function(v[0], v[1])

            F = [f, g]

            try:
                delta = np.linalg.solve(np.array(jac), -1 * np.array(F))
            except np.linalg.LinAlgError:
                raise Exception('Ошибка применения метода: Якобиан вырожден.')

            if np.max(np.abs(delta)) < eps:
                break

            next_v = v + delta

            v = next_v.tolist()

        return Result(v[0], iteration, v[1])