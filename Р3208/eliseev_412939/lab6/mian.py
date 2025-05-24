import numpy as np
import matplotlib.pyplot as plt


def f1(x, y):
    # y' = x + y, y(0)=1
    return x + y


def exact1(x):
    return 2 * np.exp(x) - x - 1


def f2(x, y):
    # y' = y - x^2 + 1, y(0)=0.5
    return y - x**2 + 1


def exact2(x):
    return 3.5 * np.exp(x) - x**2 - 2 * x - 3


def f3(x, y):
    # y' = y*(1 - y), y(0)=0.1
    return y * (1 - y)


def exact3(x):
    return 1 / (1 + 9 * np.exp(-x))


problems = {
    1: ("y' = x + y,    y(0)=1",    f1, exact1, 0.0, 1),
    2: ("y' = y - x^2+1, y(0)=0.5", f2, exact2, 0.0, 0.5),
    3: ("y' = y(1-y),    y(0)=0.1", f3, exact3, 0.0, 0.1),
}


def euler_method(f, x0, y0, h, n):
    xs = x0 + h * np.arange(n + 1)
    ys = np.zeros(n + 1)
    ys[0] = y0
    for i in range(n):
        ys[i + 1] = ys[i] + h * f(xs[i], ys[i])
    return xs, ys


def rk4_method(f, x0, y0, h, n):
    xs = x0 + h * np.arange(n + 1)
    ys = np.zeros(n + 1)
    ys[0] = y0
    for i in range(n):
        x_i, y_i = xs[i], ys[i]
        k1 = f(x_i, y_i)
        k2 = f(x_i + h/2, y_i + h*k1/2)
        k3 = f(x_i + h/2, y_i + h*k2/2)
        k4 = f(x_i + h,   y_i + h*k3)
        ys[i+1] = y_i + h*(k1 + 2*k2 + 2*k3 + k4)/6
    return xs, ys


def runge_error(f, method, x0, y0, h, n, order):
    # вычисляем y_h
    xs_h, ys_h = method(f, x0, y0, h, n)
    # считаем с шагом h/2
    n2 = int((xs_h[-1] - x0)/(h/2))
    xs_h2, ys_h2 = method(f, x0, y0, h/2, n2)
    # берём каждый второй узел из ys_h2
    ys_h2_sub = ys_h2[::2]
    # оценка по правилу Рунге
    err = np.max(np.abs(ys_h - ys_h2_sub) / (2**order - 1))
    return err


def milne_method(f, x0, y0, h, n):
    # стартуем 0..3 точками методом РК4
    xs = x0 + h * np.arange(n + 1)
    ys = np.zeros(n + 1)
    ys[:4] = rk4_method(f, x0, y0, h, 3)[1]
    for i in range(3, n):
        # индексы: i-3, i-2, i-1, i
        f_vals = [f(xs[j], ys[j]) for j in (i-3, i-2, i-1, i)]
        # предиктор Милна
        y_pred = ys[i-3] + (4*h/3)*(2*f_vals[1] - f_vals[2] + 2*f_vals[3])
        # корректор Милна
        f_pred = f(xs[i+1], y_pred)
        ys[i+1] = ys[i-1] + (h/3)*(f_vals[2] + 4*f_vals[3] + f_pred)
    return xs, ys


def main():
    print("Выберите задачу:")
    for k, v in problems.items():
        print(f" {k}: {v[0]}")
    try:
        choice = int(input("Номер задачи (1/2/3): "))
        desc, f, exact, x0_def, y0_def = problems[choice]
    except (KeyError, ValueError):
        print("Некорректный выбор задачи.")
        return

    try:
        x0 = float(input(f"Начальное x0 [{x0_def}]: ") or x0_def)
        xn = float(input("Конечное xn: "))
        if xn <= x0:
            raise ValueError("xn должно быть > x0")
        h = float(input("Шаг h: "))
        if h <= 0 or h > (xn - x0):
            raise ValueError("h должно быть >0 и <(xn-x0)")
        eps = float(input("Точность ε (для Рунге): "))
        if eps <= 0:
            raise ValueError("ε должно быть >0")
    except ValueError as e:
        print("Ошибка ввода:", e)
        return

    # вычисляем число шагов
    n = int(np.ceil((xn - x0)/h))
    h = (xn - x0)/n  # подправим шаг, чтобы точно дойти до xn

    # метод Эйлера
    xs_e, ys_e = euler_method(f, x0, y0_def, h, n)
    err_e = runge_error(f, euler_method, x0, y0_def, h, n, order=1)

    # метод РК4
    xs_rk, ys_rk = rk4_method(f, x0, y0_def, h, n)
    err_rk = runge_error(f, rk4_method, x0, y0_def, h, n, order=4)

    # метод Милна
    xs_m, ys_m = milne_method(f, x0, y0_def, h, n)
    ys_exact = exact(xs_m)
    err_m = np.max(np.abs(ys_exact - ys_m))

    # печать таблицы
    header = f"{'x':>8} {'y_exact':>12} {'Euler':>10} {'RK4':>10} {'Milne':>10}"
    print("\n" + header)
    print("-"*len(header))
    for xi, ye, yeu, yr, ym in zip(xs_m, ys_exact, ys_e, ys_rk, ys_m):
        print(f"{xi:8.4f} {ye:12.6f} {yeu:10.6f} {yr:10.6f} {ym:10.6f}")

    # вывод оценок погрешности
    print(f"\nМаксимальная оценка погрешности по Рунге (Эйлер):       {err_e:.2e}")
    print(f"Максимальная оценка погрешности по Рунге (РК4):         {err_rk:.2e}")
    print(f"Максимальная погрешность метода Милна (точное решение): {err_m:.2e}")

    # построение графиков
    plt.figure(figsize=(8, 5))
    plt.plot(xs_m, ys_exact,    label="Exact",   linewidth=2)
    plt.plot(xs_e, ys_e,        '--', label="Euler")
    plt.plot(xs_rk, ys_rk,      '-.', label="RK4")
    plt.plot(xs_m, ys_m,        ':',  label="Milne")
    plt.title(f"Решение задачи: {desc}")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    main()
