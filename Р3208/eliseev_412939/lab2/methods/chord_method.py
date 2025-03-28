from dto.equation import Equation
from dto.result import Result
from methods.method import Method, MAX_ITERATIONS


class ChordMethod(Method):
    """
    Класс для реализации метода хорд
    """
    name = 'Метод хорд'

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
        Метод хорд:
        1. находим интервал изоляции корня [a0, b0]
        2. вычисляем x0
        3. вычисляем f(x0)
        4. в качестве нового интервала выбираем ту половину отрезка, на концах которой функция имеет разные знаки
        5. вычисляем x1 и т. д. (повторяем шаги 2-4)
        :return: Результат решения — объект Result
        """
        f = self.equation.function
        a, b = self.a, self.b
        eps = self.eps
        log = self.log
        iterations = 0

        # Формула хорд
        x = (a * f(b) - b * f(a)) / (f(b) - f(a))

        while True:
            if iterations == MAX_ITERATIONS:
                raise Exception(f'Выполнено {MAX_ITERATIONS} итераций. Решение н найдено')
            iterations += 1

            # Обновляем границы
            if f(a) * f(x) <= 0:
                b = x
            else:
                a = x

            new_x = (a * f(b) - b * f(a)) / (f(b) - f(a))
            delta = abs(new_x - x)

            log.append({
                'a': a,
                'b': b,
                'x': x,
                'f(a)': f(a),
                'f(b)': f(b),
                'f(x)': f(x),
                'delta': delta
            })

            # Проверяем достижение необходимой точности
            if delta < eps:
                break

            x = new_x

        return Result(x, iterations, log)