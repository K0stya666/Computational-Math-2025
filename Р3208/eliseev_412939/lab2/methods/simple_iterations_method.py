import numpy as np
from scipy.differentiate import derivative
from dto import equation
from dto.equation import Equation
from dto.result import Result
from methods.method import Method, MAX_ITERATIONS


class SimpleIterationsMethod(Method):
    """
    Класс для реализации метода простой итерации
    """
    name = 'Метод простой итерации'

    def __init__(self, equation: Equation, a: float, b: float,
                 eps: float, decimal_places: int, log: list):
        self.equation = equation
        self.a = a
        self.b = b
        self.eps = eps
        self.decimal_places = decimal_places
        self.log = log

        super().__init__(equation, a, b, eps, decimal_places, log)

    def check(self):
        """
        Проверка наличия корня на заданном отрезке.
        :return: Кортеж (успешность проверки, сообщение)
        """
        if not self.equation.root_exists(self.a, self.b):
            return False, 'Корень на заданном промежутке отсутствует или их > 2'
        return True, ''

    def solve(self) -> Result:
        """
        Метод простой итераций:
        1. преобразуем уравнение f(x) = 0 к равносильному (при _lambda != 0) _lambda * f(x) = 0
        2. прибавляем x в обеих частях: x = x + _lambda * f(x)
        3. phi(x) = x + _lambda * f(x), phi'(x) = 1 + _lambda * f'(x)
        4. высокая сходимость  обеспечивается при q = max(|phi'(x)|) примерно равное 0. Тогда _lambda = 1/max(|f'(x)|) (с минусом, если f'[a, b] > 0)
        :return: Результат решения — объект Result
        """
        f = self.equation.function
        f_ = equation.snd_derivative
        a = self.a
        b = self.b
        eps = self.eps
        log = self.log
        iterations = 0

        max_derivative = max(abs(f_(a)), abs(f_(b)))
        _lambda = 1 / max_derivative
        if f_(a) > 0: _lambda *= -1

        phi = lambda x: x + _lambda * f(x)
        phi_ = lambda x: derivative(phi, x).df

        q = np.max(abs(phi_(np.linspace(a, b, int(1 / eps)))))
        if q > 1:
            raise Exception(f'Метод не сходится, так как q >= 1')

        prev_x = a

        while True:
            if iterations == MAX_ITERATIONS:
                raise Exception(f'Выполнено {MAX_ITERATIONS} итераций. Решение н найдено')
            iterations += 1

            x = phi(prev_x)
            delta = abs(x - prev_x)

            log.append({
                'x_i': prev_x,
                'x_(i+1)': x,
                'phi(x_(i+1))': phi(x),
                'f(x_(i+1))': f(x),
                'delta': delta
            })

            if delta < eps:
                break

            prev_x = x

        return Result(x, iterations, log)

