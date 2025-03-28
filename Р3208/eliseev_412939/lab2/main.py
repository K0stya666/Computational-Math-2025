import matplotlib.pyplot as plt
from scipy.differentiate import derivative
import numpy as np
from dto.equation import Equation
from dto.result import Result
from methods.simple_iterations_method import SimpleIterationsMethod

# MAX_ITERATIONS = 1000

# Методы решения
methods = {
    1: ChordMethod,
    2: SecantMethod,
    3: SimpleIterationsMethod,
    4: NewtonMethod,
}

# Одномерные нелинейные уравнения
equations = {
    1: Equation(lambda x: (x**3 - 1.89*x**2 - 2*x + 1.76), 'x^3 - 1.89*x^2 - 2*x + 1.76'),
    2: Equation(lambda x: (-1.38*x**3 - 5.42*x**2 + 2.57*x + 10.95), '-1.38*x^3 - 5.42*x^2 + 2.57*x + 10.95'),
    3: Equation(lambda x: (-1.8*x**3 - 2.94*x**2 + 10.37*x + 5.38), '-1.8*x^3 - 2.94*x^2 + 10.37*x + 5.38'),
}


def chord_method(equation, a, b, eps):
    """
    Метод хорд для решения f(x)=0 на [a, b].
    Возвращает (x, итерации).
    """
    f = equation.function
    iterations = 0
    log = []

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
    #         a = x
    #
    #     new_x = (a * f(b) - b * f(a)) / (f(b) - f(a))
    #     delta = abs(new_x - x)
    #
    #     log.append({
    #         'a': a,
    #         'b': b,
    #         'x': x,
    #         'f(a)': f(a),
    #         'f(b)': f(b),
    #         'f(x)': f(x),
    #         'delta': delta
    #     })
    #
    #     # Проверяем достижение необходимой точности
    #     if delta < eps:
    #         break
    #
    #     x = new_x
    #
    # return Result(x, iterations, log)


def secant_method(equation, a, b, eps):
    """
    Метод секущих.
    Возвращает (x, итерации).
    """
    f = equation.function
    f__ = equation.snd_derivative
    iterations = 0
    log = []

    # Проверяем условие сходимости метода
    if f__(a) * f__(b) < 0:
        raise Exception('Условие сходимости метода секущих не выполнено')

    x0 = a
    if f(a) * f__(b) > 0:
        x0 = a
    if f(b) * f__(b) > 0:
        x0 = b

    x1 = x0 + eps

    while True:
        if iterations == MAX_ITERATIONS:
            raise Exception(f'Выполнено {MAX_ITERATIONS} итераций. Решение н найдено')
        iterations += 1

        x = x1 - f(x1) * (x1 - x0) / (f(x1) - f(x0))
        delta = abs(x - x1)

        log.append({
            'x_(i-1)': x0,
            'x_i': x1,
            'x_(i+1)': x,
            'f(x_(i+1))': f(x),
            'delta': delta
        })

        # Проверяем достижение необходимой точности
        if delta < eps:
            break

        x0 = x1
        x1 = x

    return Result(x, iterations, log)


# ---------------------------------------------------
#             МЕТОД ПРОСТОЙ ИТЕРАЦИИ
# ---------------------------------------------------

# def simple_iteration_method(equation, a, b, eps):
#     """
#     Метод простой итерации:
#     Необходимо заранее задать итерационную функцию g(x) так,
#     чтобы |g'(x)| < 1 на рассматриваемом отрезке.
#     Для простоты возьмём g(x) = x - alpha * f(x),
#     где alpha - некоторая константа, которую оценим.
#     """
#     f = equation.function
#     f_ = equation.snd_derivative
#     iterations = 0
#     log = []
#
#     max_derivative = max(abs(f_(a)), abs(f_(b)))
#     _lambda = 1 / max_derivative
#     if f_(a) > 0: _lambda *= -1
#
#     phi = lambda x: x + _lambda * f(x)
#     phi_ = lambda x: derivative(phi, x).df
#
#     q = np.max(abs(phi_(np.linspace(a, b, int(1 / eps)))))
#     if q > 1:
#         raise Exception(f'Метод не сходится, так как q >= 1')
#
#     prev_x = a
#
#     while True:
#         if iterations == MAX_ITERATIONS:
#             raise Exception(f'Выполнено {MAX_ITERATIONS} итераций. Решение н найдено')
#         iterations += 1
#
#         x = phi(prev_x)
#         delta = abs(x - prev_x)
#
#         log.append({
#             'x_i': prev_x,
#             'x_(i+1)': x,
#             'phi(x_(i+1))': phi(x),
#             'f(x_(i+1))': f(x),
#             'delta': delta
#         })
#
#         if delta < eps:
#             break
#
#         prev_x = x
#
#     return Result(x, iterations, log)

# ---------------------------------------------------
#                МЕТОД НЬЮТОНА (1D)
# ---------------------------------------------------
def newton_method_1d(f, x0, eps=1e-6, max_iter=1000):
    """
    Одномерный метод Ньютона.
    Потребуется численно оценивать f'(x).
    """

    def derivative(func, x, h=1e-6):
        return (func(x + h) - func(x)) / h

    x_cur = x0
    for i in range(1, max_iter + 1):
        f_val = f(x_cur)
        df_val = derivative(f, x_cur)
        if abs(df_val) < 1e-15:
            raise ZeroDivisionError("Производная близка к 0, метод Ньютона невозможен.")
        x_next = x_cur - f_val / df_val
        if abs(x_next - x_cur) < eps or abs(f(x_next)) < eps:
            return x_next, i
        x_cur = x_next
    return x_cur, max_iter


# ===================================================
#       СИСТЕМЫ НЕЛИНЕЙНЫХ УРАВНЕНИЙ + МЕТОД НЬЮТОНА
# ===================================================

# Пример 1
def F1_system1(xy):
    """ F1(x, y) = x^2 + y^2 - 4 = 0 """
    x, y = xy
    return x ** 2 + y ** 2 - 4


def F2_system1(xy):
    """ F2(x, y) = x - y = 0 """
    x, y = xy
    return x - y


# Пример 2
def F1_system2(xy):
    """ x^2 + y^2 - 1 = 0 """
    x, y = xy
    return x ** 2 + y ** 2 - 1


def F2_system2(xy):
    """ x^3 - y = 0 """
    x, y = xy
    return x ** 3 - y


systems_2d = {
    1: ("Система 1:\n  { x^2 + y^2 = 4\n  { x - y = 0", (F1_system1, F2_system1)),
    2: ("Система 2:\n  { x^2 + y^2 = 1\n  { x^3 - y = 0", (F1_system2, F2_system2)),
    # Можно добавить третью систему при необходимости
}


def jacobian_2d(F1, F2, x, y, h=1e-6):
    """
    Численно вычисляем Якобиан:
    J = [ [dF1/dx, dF1/dy],
          [dF2/dx, dF2/dy] ]
    """

    def dFdx(F, x_, y_):
        return (F((x_ + h, y_)) - F((x_, y_))) / h

    def dFdy(F, x_, y_):
        return (F((x_, y_ + h)) - F((x_, y_))) / h

    j11 = dFdx(F1, x, y)
    j12 = dFdy(F1, x, y)
    j21 = dFdx(F2, x, y)
    j22 = dFdy(F2, x, y)
    return np.array([[j11, j12],
                     [j21, j22]])


def newton_method_2d(F1, F2, x0, y0, eps=1e-6, max_iter=100):
    """
    Метод Ньютона для системы из двух уравнений F1=0, F2=0.
    (x, y) -> (x - J^-1 * F(x))
    где F(x) = (F1, F2).
    """
    xy = np.array([x0, y0], dtype=float)
    for i in range(1, max_iter + 1):
        f_val = np.array([F1(xy), F2(xy)])
        # Если норма вектора F мала - решение найдено
        if np.linalg.norm(f_val, ord=2) < eps:
            return xy, i
        # Якобиан
        J = jacobian_2d(F1, F2, xy[0], xy[1])
        if abs(np.linalg.det(J)) < 1e-15:
            raise ZeroDivisionError("Якобиан вырожден, метод Ньютона не применим.")
        # Решаем систему J * delta = F_val
        # xy_{new} = xy - delta
        delta = np.linalg.solve(J, f_val)
        xy_new = xy - delta
        if np.linalg.norm(xy_new - xy, ord=2) < eps:
            return xy_new, i
        xy = xy_new
    return xy, max_iter


# ===================================================
#             ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ===================================================

def sign_change_exists(f, a, b, steps=200):
    """
    Грубая проверка существования смены знака на [a, b].
    Возвращаем:
      -1, если корней нет или >1 (т.е. знак меняется более одного раза),
       1, если ровно один корень (одна смена знака),
       0, если не удалось надёжно определить.
    """
    x_vals = np.linspace(a, b, steps + 1)
    f_vals = [f(x) for x in x_vals]
    sign_changes = 0
    for i in range(len(f_vals) - 1):
        if f_vals[i] * f_vals[i + 1] < 0:
            sign_changes += 1
    if sign_changes == 1:
        return 1
    elif sign_changes == 0:
        return 0
    else:
        return -1


def plot_1d_function(f, a, b, root=None):
    """
    Построение графика f(x) на интервале [a,b].
    Optionally отмечаем корень.
    """
    x_vals = np.linspace(a, b, 400)
    y_vals = [f(x) for x in x_vals]
    plt.axhline(0, color='black', linewidth=0.8)
    plt.plot(x_vals, y_vals, label="f(x)")
    if root is not None:
        plt.plot(root, f(root), 'ro', label="Найденный корень")
    plt.title("График f(x) на [" + str(a) + ", " + str(b) + "]")
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.legend()
    plt.grid(True)
    plt.show()


def plot_2d_system(F1, F2, x_range=(-3, 3), y_range=(-3, 3), solution=None):
    """
    Простое построение кривых F1(x,y)=0 и F2(x,y)=0 на сетке x_range x y_range.
    """
    x_vals = np.linspace(x_range[0], x_range[1], 300)
    y_vals = np.linspace(y_range[0], y_range[1], 300)
    X, Y = np.meshgrid(x_vals, y_vals)
    Z1 = np.zeros_like(X)
    Z2 = np.zeros_like(X)
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            Z1[i, j] = F1((X[i, j], Y[i, j]))
            Z2[i, j] = F2((X[i, j], Y[i, j]))

    plt.contour(X, Y, Z1, levels=[0], colors='red')
    plt.contour(X, Y, Z2, levels=[0], colors='blue')
    if solution is not None:
        plt.plot(solution[0], solution[1], 'ko', label="Решение")
    plt.title("График системы F1=0 (красная) и F2=0 (синяя)")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.grid(True)
    plt.show()


# ===================================================
#                       MAIN
# ===================================================
def main():
    print("Выберите режим:")
    print("1) Решение одиночного нелинейного уравнения")
    print("2) Решение системы нелинейных уравнений (2D)")
    mode = input("Ваш выбор (1/2): ").strip()

    if mode == "1":
        # -----------------------
        # ОДНОМЕРНЫЙ СЛУЧАЙ
        # -----------------------
        print("Список доступных функций:")
        for k, (func, desc) in equations.items():
            print(f"{k}) f(x) = {desc}")
        choice = int(input("Выберите номер функции: "))
        if choice not in equations:
            print("Нет такой функции.")
            return
        desc, f = equations[choice]

        # Ввод интервала, eps
        print("Введите границы интервала (a, b):")
        a = float(input("a = "))
        b = float(input("b = "))
        if a > b:
            a, b = b, a
        print("Введите требуемую точность eps (напр. 1e-6):")
        eps = float(input("eps = "))

        # Проверка наличия корня
        sc = sign_change_exists(f, a, b)
        if sc == 0:
            print("На отрезке нет смены знака, возможно, корней нет.")
        elif sc == -1:
            print("На отрезке вероятно несколько корней. Метод применён будет к первому найденному.")
        else:
            print("На отрезке ровно одна смена знака.")

        # Выбор метода
        print("Выберите метод:")
        print("1) Хорд")
        print("2) Секущих")
        print("3) Простой итерации")
        print("4) Ньютона (1D)")
        method_choice = input("Ваш выбор: ").strip()

        if method_choice == "1":
            root, iters = chord_method(f, a, b, eps)
        elif method_choice == "2":
            # Нужно задать два начальных приближения x0, x1
            x0 = a
            x1 = b
            root, iters = secant_method(f, x0, x1, eps)
        elif method_choice == "3":
            root, iters = simple_iteration_method(f, a, b, eps)
        elif method_choice == "4":
            # Выбираем начальное приближение, возьмём середину
            x0 = (a + b) / 2
            root, iters = newton_method_1d(f, x0, eps)
        else:
            print("Неверный выбор метода.")
            return

        # Вывод результатов
        f_root = f(root)
        print(f"Найден корень: x = {root}")
        print(f"f(x) = {f_root}")
        print(f"Число итераций: {iters}")

        # Хотим ли вывод в файл или на экран? Уже вывели на экран;
        # для примера покажем простую запись в файл:
        save_choice = input("Сохранить результат в файл? (y/n): ").strip().lower()
        if save_choice == "y":
            with open("result_1d.txt", "w", encoding="utf-8") as fw:
                fw.write(f"Функция: {desc}\n")
                fw.write(f"Найден корень: {root}\n")
                fw.write(f"f(корень) = {f_root}\n")
                fw.write(f"Число итераций: {iters}\n")

        # Построим график
        plot_1d_function(f, a, b, root)

    elif mode == "2":
        # -----------------------
        # СИСТЕМА 2D
        # -----------------------
        print("Список доступных систем:")
        for k, (desc, (F1, F2)) in systems_2d.items():
            print(f"{k}) {desc}")
        choice = int(input("Выберите номер системы: "))
        if choice not in systems_2d:
            print("Нет такой системы.")
            return
        desc, (F1, F2) = systems_2d[choice]

        print("Введите начальные приближения x0, y0 (через пробел):")
        x0, y0 = map(float, input().split())

        print("Введите точность eps:")
        eps = float(input("eps = "))

        # Метод Ньютона для системы
        solution, iters = newton_method_2d(F1, F2, x0, y0, eps)
        print(f"Решение системы: (x, y) = ({solution[0]}, {solution[1]})")
        print(f"Число итераций: {iters}")
        print(f"Проверка F1: {F1(solution)}, F2: {F2(solution)}")

        # Вывод в файл?
        save_choice = input("Сохранить результат в файл? (y/n): ").strip().lower()
        if save_choice == "y":
            with open("result_2d.txt", "w", encoding="utf-8") as fw:
                fw.write(f"{desc}\n")
                fw.write(f"Найдено решение (x, y) = {solution}\n")
                fw.write(f"Число итераций: {iters}\n")
                fw.write(f"F1(solution) = {F1(solution)}, F2(solution) = {F2(solution)}\n")

        # Построим графики кривых F1=0 и F2=0
        # Пользователь может задать диапазон для построения,
        # здесь для примера возьмём [-5,5] x [-5,5].
        plot_2d_system(F1, F2, x_range=(-5, 5), y_range=(-5, 5), solution=solution)
    else:
        print("Неверный выбор режима.")


if __name__ == "__main__":
    main()
