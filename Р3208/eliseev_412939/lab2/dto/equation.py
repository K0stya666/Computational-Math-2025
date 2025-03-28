from typing import Callable
import numpy as np
import matplotlib.pyplot as plt
from scipy.differentiate import derivative


class Equation:
    """
    Класс представляющий мат. функцию и её описание
    """

    def __init__(self, function: Callable, description: str):
        self.function = function
        self.description = description


    def draw(self, a: float, b: float):
        """
        Строит график функции на отрезке [a, b].
        :param a: Левая граница отображаемого интервала.
        :param b: Правая граница отображаемого интервала.
        """
        x = np.linspace(a, b)
        func = np.vectorize(self.function)(x)

        plt.title = 'График заданной функции'
        plt.grid(True, which='both')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.axhline(y=0, color='gray', label='y = 0')
        plt.plot(x, func, 'blue', label=self.description)
        plt.legend(loc='upper left')
        plt.savefig('graph.png')
        plt.show()

    def root_exists(self, a: float, b: float):
        """
        Проверяет наличие корня функции на отрезке [a, b] по признаку смены знака.
        :param a: Левая граница отрезка.
        :param b: Правая граница отрезка.
        :return: True, если функция имеет решения на выбранном отрезке.
        """
        f = self.function

        fa = f(a)
        fb = f(b)

        fa_ = derivative(f, a).df
        fb_ = derivative(f, b).df

        return (fa * fb < 0) and (fa_ * fb_ > 0)