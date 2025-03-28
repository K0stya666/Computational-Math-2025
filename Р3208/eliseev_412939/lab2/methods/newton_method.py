from dto.equation import Equation
from dto.result import Result
from methods.method import Method


class NewtonMethod(Method):
    """
    Класс для реализации метода Ньютона
    """
    name = "Метод Ньютона"

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

        :return:
        """
