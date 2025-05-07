import sys
import matplotlib.pyplot as plt
import numpy as np
from data_loader import load_from_keyboard, load_from_file, load_from_function
from interpolation import diff_table, lagrange, newton_divided, newton_forward, newton_backward

def print_diff_table(xs, ys):
    table = diff_table(xs, ys)
    print("Таблица конечных разностей:")
    for i in range(len(table)):
        row = [f"{table[i,j]:.6g}" if j <= len(table)-i-1 else "" for j in range(len(table))]
        print("\t".join(v for v in row if v))
    return table


def main():
    print("Выберите источник данных:")
    print("1: С клавиатуры")
    print("2: Из файла")
    print("3: Из функции")
    choice = input("Выбор: ")
    if choice == '1':
        xs, ys = load_from_keyboard()
    elif choice == '2':
        fname = input("Введите имя файла: ")
        xs, ys = load_from_file(fname)
    else:
        xs, ys = load_from_function()

    table = print_diff_table(xs, ys)
    x0 = float(input("Введите значение аргумента x0 для интерполяции: "))
    y_l = lagrange(xs, ys, x0)
    y_nd = newton_divided(xs, ys, x0)
    y_nf = newton_forward(xs, ys, x0)
    y_nb = newton_backward(xs, ys, x0)

    print(f"\nРезультаты интерполяции в точке {x0}:")
    print(f"Лагранж: {y_l}")
    print(f"Ньютон (разделённые разности): {y_nd}")
    print(f"Ньютон (вперёд): {y_nf}")
    print(f"Ньютон (назад): {y_nb}\n")

    # Построение графиков
    fig, ax = plt.subplots()
    ax.plot(xs, ys, 'o', label='Узлы интерполяции')
    X = np.linspace(min(xs), max(xs), 200)
    Y = [newton_divided(xs, ys, xi) for xi in X]
    ax.plot(X, Y, label='Ньютон интерполянт')
    ax.set_title('Интерполяция функции')
    ax.legend()
    plt.xlabel('x')
    plt.ylabel('y')
    plt.grid(True)
    plt.show()

    # Анализ результатов
    print("Анализ: абсолютные разницы между методами:")
    print(f"|Лагранж - Ньютон (разделённые)| = {abs(y_l-y_nd):.6g}")
    print(f"|Лагранж - Ньютон (вперёд)| = {abs(y_l-y_nf):.6g}")

if __name__ == '__main__':
    main()