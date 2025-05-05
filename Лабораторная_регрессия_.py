import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# 1. Генерация данных с шумом
np.random.seed(42)
x_min, x_max, points = 0, 10, 100
x = np.linspace(x_min, x_max, points)
a_true, b_true, c_true = 4, 1.5, 2  # Истинные параметры
y_true = a_true * np.sin(b_true * x) + c_true
e = np.random.uniform(-3, 3, size=x.shape)
y = y_true + e

# 2. Функции для MSE и производных
def mse(y_pred, y_true):
    return np.mean((y_pred - y_true)**2)

def get_da(x, y, a, b, c):
    return 2 * np.mean((a * np.sin(b * x) + c - y) * np.sin(b * x))

def get_db(x, y, a, b, c):
    return 2 * np.mean((a * np.sin(b * x) + c - y) * a * x * np.cos(b * x))

def get_dc(x, y, a, b, c):
    return 2 * np.mean(a * np.sin(b * x) + c - y)

# 3. Градиентный спуск
def fit(speed, epochs, a_init, b_init, c_init):
    a, b, c = a_init, b_init, c_init
    a_list, b_list, c_list = [a], [b], [c]
    for _ in range(epochs):
        da = get_da(x, y, a, b, c)
        db = get_db(x, y, a, b, c)
        dc = get_dc(x, y, a, b, c)
        a -= speed * da
        b -= speed * db
        c -= speed * dc
        a_list.append(a)
        b_list.append(b)
        c_list.append(c)
    return a_list, b_list, c_list

# Инициализация параметров
speed = 0.01
epochs = 500
a_init, b_init, c_init = 1.0, 1.0, 0.0  # Начальные приближения

a_list, b_list, c_list = fit(speed, epochs, a_init, b_init, c_init)

# 4. Визуализация с ползунком
fig, ax = plt.subplots(figsize=(10, 6))
plt.subplots_adjust(bottom=0.25)

# Исходные данные
ax.scatter(x, y, label='Исходные точки', color='gray', alpha=0.6)
line, = ax.plot(x, a_true * np.sin(b_true * x) + c_true, 'r--', label='Истинная функция')
pred_line, = ax.plot(x, a_list[0] * np.sin(b_list[0] * x) + c_list[0], 'g', label='Предсказание')
ax.legend()

# Настройка ползунка
ax_epoch = plt.axes([0.2, 0.1, 0.6, 0.03])
epoch_slider = Slider(
    ax=ax_epoch,
    label='Эпоха',
    valmin=0,
    valmax=epochs,
    valinit=0,
    valstep=1
)

# Обновление графика при движении ползунка
def update(val):
    epoch = int(epoch_slider.val)
    a = a_list[epoch]
    b = b_list[epoch]
    c = c_list[epoch]
    pred_line.set_ydata(a * np.sin(b * x) + c)
    fig.canvas.draw_idle()

epoch_slider.on_changed(update)
plt.show()

# Вывод итоговых параметров и MSE
a_final, b_final, c_final = a_list[-1], b_list[-1], c_list[-1]
y_pred = a_final * np.sin(b_final * x) + c_final
print(f"Оптимальные параметры: a={a_final:.2f}, b={b_final:.2f}, c={c_final:.2f}")
print(f"MSE: {mse(y_pred, y):.2f}")