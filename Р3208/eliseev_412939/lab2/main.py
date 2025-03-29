import matplotlib.pyplot as plt
import numpy as np
from dto.equation import Equation
from methods.chord_method import ChordMethod
from methods.newton_method import NewtonMethod
from methods.secant_method import SecantMethod
from methods.simple_iterations_method import SimpleIterationsMethod

# Методы решения
methods = {
    1: ChordMethod,
    2: SecantMethod,
    3: SimpleIterationsMethod,
    4: NewtonMethod,
}

# Одномерные нелинейные уравнения
equations = {
    1: Equation(lambda x: (x**3 - 1.89*x**2 - 2*x + 1.76), 'x^3 - 1.89 * x^2 - 2 * x + 1.76'),
    2: Equation(lambda x: (-1.38*x**3 - 5.42*x**2 + 2.57*x + 10.95), '-1.38 * x^3 - 5.42 * x^2 + 2.57 * x + 10.95'),
    3: Equation(lambda x: (-1.8*x**3 - 2.94*x**2 + 10.37*x + 5.38), '-1.8 * x^3 - 2.94 * x^2 + 10.37 * x + 5.38'),
    4: Equation(lambda x: (x**3 + 2.84*x**2 - 5.606 * x - 14.766), 'x^3 + 2.84 * x^2 - 5.606 * x - 14.766'),
}

# Системы уравнений
systems = {
    1: [
        Equation(lambda x, y: (np.tan(x * y + 0.1) - y - 1.2), 'tg(x * y + 0.1) - y = 1.2'),
        Equation(lambda x, y: (x**2 + 2 * y**2 - 1), 'x^2 + 2 * y^2 = 1'),
    ],
    2: [
        Equation(lambda x, y: (np.tan(x * y + 0.1) - y), 'tg(x * y) - y = 0'),
        Equation(lambda x, y: (x**2 + 2 * y**2 ), 'x^2 + 2 * y^2 = 0'),
    ],
    3: [
        Equation(lambda x, y: x ** 2 + y ** 2 - 4, 'x^2 + y^2 = 4'),
        Equation(lambda x, y: -3 * x ** 2 + y, 'y = 3x^2'),
    ]
}







# ===================================================
#             ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ===================================================



def plot_function(f, a, b, root=None):
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


def plot_system(F1, F2, x_range=(-3, 3), y_range=(-3, 3), solution=None):
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
    print("1 - Решение нелинейного уравнения")
    print("2 - Решение системы нелинейных уравнений (Методом Ньютона)")
    mode = input("Ваш выбор (1/2): ").strip()

    if mode == "1":
        # -----------------------
        # ОДНОМЕРНЫЙ СЛУЧАЙ
        # -----------------------
        print("Список доступных функций:")
        for k, eq in equations.items():
            print(f"{k}) f(x) = {eq.description}")
        choice = int(input("Выберите номер функции: "))
        if choice not in equations:
            print("Нет такой функции.")
            return
        equation = equations[choice]
        f = equation.function
        desc = equation.description

        is_exist = False
        global a, b
        while not is_exist:
            print("Введите границы интервала [a, b]:")
            a = float(input("a = "))
            b = float(input("b = "))
            if not equation.root_exists(a, b):
                print("ВНИМАНИЕ: На выбранном отрезке нет решения для данного уравнения. Попробуйте ввести другие значения a, b.")
            else:
                is_exist = True

        print("Введите требуемую точность eps:")
        eps = float(input("eps = "))
        decimal_place = int(input("Введите количество знаков после запятой: "))

        # Выбор метода
        print("Выберите метод:")
        print("1 - Хорд")
        print("2 - Секущих")
        print("3 - Простой итерации")
        method_choice = int(input("Ваш выбор: ").strip())

        if method_choice != 1 and method_choice != 2 and method_choice != 3:
            print("Нет такого метода")
            return


        method = methods[method_choice](equation, a, b, eps, decimal_place)
        res = method.solve()

        # Вывод результатов
        root = res.x
        iters = res.iterations
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
        plot_function(f, a, b, root)

    elif mode == "2":
        # -----------------------
        # СИСТЕМА
        # -----------------------
        print("Список доступных систем:")
        for k, sys in systems.items():
            print(f"{k}) {sys[0].description} and {sys[1].description}")
        choice = int(input("Выберите номер системы: "))
        if choice not in systems:                    # <---------------
            print("Нет такой системы.")
            return

        sys = systems[choice]
        f1 = sys[0].function
        desc1 = sys[0].description
        f2 = sys[1].function
        desc2 = sys[1].description
        desc = desc1 + " and " + desc2

        # print("Введите начальные приближения x0, y0 (через пробел):")
        # x0, y0 = map(float, input().split())

        print("Введите точность eps:")
        eps = float(input("eps = "))

        # Метод Ньютона для системы
        methode = methods[4](sys, eps)
        res = methode.solve()

        iters = res.iterations
        x = res.x
        y = res.y

        print(f"Решение системы: (x, y) = ({x}, {y}")
        print(f"Число итераций: {iters}")

        # Вывод в файл?
        save_choice = input("Сохранить результат в файл? (y/n): ").strip().lower()
        if save_choice == "y":
            with open("result_2d.txt", "w", encoding="utf-8") as fw:
                fw.write(f"{desc}\n")
                fw.write(f"Найдено решение (x, y) = {x}, {y}\n")
                fw.write(f"Число итераций: {iters}\n")
                fw.write(f"F1(solution) = {f1(x,y)}, F2(solution) = {f2(x,y)}\n")

        # Построим графики кривых F1=0 и F2=0
        # Пользователь может задать диапазон для построения,
        # здесь для примера возьмём [-5,5] x [-5,5].
        plot_system(f1, f2, x_range=(-5, 5), y_range=(-5, 5), solution=[x])
    else:
        print("Неверный выбор режима.")


if __name__ == "__main__":
    main()
