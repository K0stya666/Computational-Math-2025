from function import Function
from methods.rectangle_method import RectangleMethod
from methods.simpson_method import SimpsonMethod
from methods.trapezoid_method import TrapezoidMethod


# функции
functions = {
    1: Function(
        lambda x: -x ** 3 - x ** 2 - 2 * x + 1,
        "f(x) = -x^3 - x^2 - 2x + 1"
    ),
    2: Function(
        lambda x: -3 * x ** 3 - 5 * x ** 2 + 4 * x - 2,
        "f(x) = -3x^3 - 5x^2 + 4x - 2"
    ),
    3: Function(
        lambda x: -x ** 3 - x ** 2 + x + 3,
        "f(x) = -x^3 - x^2 + x + 3"
    )
}


def runge_integration(method_obj, f, a, b, eps):
    """
    Адаптивное интегрирование с использованием правила Рунге:
    method_obj  - объект класса (RectangleMethod / TrapezoidMethod / SimpsonMethod)
                  который имеет:
                  * метод .integrate(f, a, b, n)
                  * атрибут .order (порядок точности p)
    f           - функция (экземпляр MathFunction или любая callable)
    a, b        - пределы интегрирования
    eps         - требуемая точность
    Возвращает (I, n), где I - значение интеграла, n - использованное число разбиений.
    """
    p = method_obj.order
    R = 2 ** p - 1  # Коэффициент Рунге
    n = 4  # Начальное число разбиений

    I_prev = method_obj.integrate(f, a, b, n)

    while True:
        n *= 2
        I_curr = method_obj.integrate(f, a, b, n)
        error_est = abs(I_curr - I_prev) / R
        if error_est < eps:
            return I_curr, n
        I_prev = I_curr


def main():
    print("Выберите функцию для интегрирования:")
    for num, mf in functions.items():
        print(f"{num}) {mf.description}")
    func_choice = int(input("Введите номер функции: "))

    if func_choice not in functions:
        print("Неверный выбор, завершаем.")
        return

    f = functions[func_choice]

    print("\nВыберите метод численного интегрирования:")
    print("1 - Метод левых прямоугольников")
    print("2 - Метод правых прямоугольников")
    print("3 - Метод средних прямоугольников")
    print("4 - Метод трапеций")
    print("5 - Метод Симпсона")
    method_choice = int(input("Введите номер метода: "))

    # Создаём объект соответствующего метода
    if method_choice == 1:
        method_obj = RectangleMethod(mode='left')
        method_name = "Левые прямоугольники"
    elif method_choice == 2:
        method_obj = RectangleMethod(mode='right')
        method_name = "Правые прямоугольники"
    elif method_choice == 3:
        method_obj = RectangleMethod(mode='middle')
        method_name = "Средние прямоугольники"
    elif method_choice == 4:
        method_obj = TrapezoidMethod()
        method_name = "Трапеции"
    elif method_choice == 5:
        method_obj = SimpsonMethod()
        method_name = "Симпсон"
    else:
        print("Неверный выбор метода. Завершаем.")
        return

    # Считываем пределы интегрирования
    print("\nВведите пределы интегрирования a и b:")
    a = float(input("a = "))
    b = float(input("b = "))

    # Считываем точность
    eps = float(input("\nВведите требуемую точность eps: "))

    # Выполняем интегрирование с правилом Рунге
    result, n_final = runge_integration(method_obj, f, a, b, eps)

    print(f"\nРезультаты вычисления методом: {method_name}")
    print(f"Функция: {f.description}")
    print(f"Интеграл на отрезке [{a}; {b}] ≈ {result:.8f}")
    print(f"Достигнуто при числе разбиений n = {n_final}")
    print(f"Заданная точность: eps = {eps}")


if __name__ == "__main__":
    main()
