import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
import math


class MatrixTransform:
    @staticmethod
    def multiply_matrix_vector(matrix, vector):
        """Умножение матрицы 3x3 на вектор 1x3"""
        return [
            matrix[0][0] * vector[0] + matrix[0][1] * vector[1] + matrix[0][2] * vector[2],
            matrix[1][0] * vector[0] + matrix[1][1] * vector[1] + matrix[1][2] * vector[2],
            matrix[2][0] * vector[0] + matrix[2][1] * vector[1] + matrix[2][2] * vector[2]
        ]

    @staticmethod
    def create_rotation_around_point_matrix(angle_degrees, cx, cy):
        """Матрица поворота относительно точки (cx, cy)"""
        angle_rad = math.radians(angle_degrees)
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)

        return [
            [cos_a, -sin_a, cx * (1 - cos_a) + cy * sin_a],
            [sin_a, cos_a, cy * (1 - cos_a) - cx * sin_a],
            [0, 0, 1]
        ]

    @staticmethod
    def apply_transform(points_matrix, transform_matrix):
        """Применение преобразования ко всем вершинам"""
        transformed = []
        for vertex in points_matrix:
            new_vertex = MatrixTransform.multiply_matrix_vector(transform_matrix, vertex)
            transformed.append(new_vertex)
        return transformed


# Создаем фигуру
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)
ax.set_axis_off()
ax.set_aspect('equal')

# Параметры
prop_angle = 0

# Задняя часть
back = patches.Circle((0, 3), 0.5, facecolor='grey', edgecolor='black', linewidth=2)
ax.add_patch(back)

# Хвост вертикальный
tail_vertical, = ax.plot([0, 0], [3.5, 4.5], 'black', linewidth=4, solid_capstyle='round')

# Фюзеляж
fuselage = patches.Circle((0, 1), 2, facecolor='grey', edgecolor='black', linewidth=2)
ax.add_patch(fuselage)

# Стабилизаторы
tail_h_left, = ax.plot([-5, -5], [0, -2], 'black', linewidth=8, solid_capstyle='round')
tail_h_right, = ax.plot([5, 5], [0, -2], 'black', linewidth=8, solid_capstyle='round')

# Крылья
wing_left, = ax.plot([-9, -2], [0, 0], 'black', linewidth=15, solid_capstyle='round')
wing_right, = ax.plot([2, 9], [0, 0], 'black', linewidth=15, solid_capstyle='round')

# Хвостовые стабилизаторы
tail_h1_left, = ax.plot([-4, -1.8], [2, 2], 'black', linewidth=7, solid_capstyle='round')
tail_h1_right, = ax.plot([1.8, 4], [2, 2], 'black', linewidth=7, solid_capstyle='round')

# Колеса
wheel_left = patches.Circle((-5, -2.5), 0.5, facecolor='grey', edgecolor='black', linewidth=2)
wheel_right = patches.Circle((5, -2.5), 0.5, facecolor='grey', edgecolor='black', linewidth=2)
ax.add_patch(wheel_left)
ax.add_patch(wheel_right)

# Точки винта
center_point = [0, 1, 1]  # центр винта
blade_length = 3.5

# Концы лопастей (начальное положение)
blade1_end = [blade_length, 1, 1]  # 0°
blade2_end = [-blade_length / 2, 1 + blade_length * math.sqrt(3) / 2, 1]  # 120°
blade3_end = [-blade_length / 2, 1 - blade_length * math.sqrt(3) / 2, 1]  # 240°

propeller_points = [blade1_end, blade2_end, blade3_end]

# Создаем линии для лопастей
propeller_blade1, = ax.plot([], [], 'brown', linewidth=8, solid_capstyle='round')
propeller_blade2, = ax.plot([], [], 'brown', linewidth=8, solid_capstyle='round')
propeller_blade3, = ax.plot([], [], 'brown', linewidth=8, solid_capstyle='round')
propeller_center = ax.scatter([center_point[0]], [center_point[1]], color='black', s=150, zorder=10)


def animate(_):
    global prop_angle

    # Вращение винта
    prop_angle += 18

    # Матрица поворота относительно точки (0, 1)
    rotation_matrix = MatrixTransform.create_rotation_around_point_matrix(
        prop_angle, center_point[0], center_point[1]
    )

    # Применяем матрицу ко всем точкам винта
    rotated_points = MatrixTransform.apply_transform(propeller_points, rotation_matrix)

    # Рисуем лопасти
    propeller_blade1.set_data([center_point[0], rotated_points[0][0]],
                              [center_point[1], rotated_points[0][1]])
    propeller_blade2.set_data([center_point[0], rotated_points[1][0]],
                              [center_point[1], rotated_points[1][1]])
    propeller_blade3.set_data([center_point[0], rotated_points[2][0]],
                              [center_point[1], rotated_points[2][1]])

    return (propeller_blade1, propeller_blade2, propeller_blade3, propeller_center,
            tail_vertical, tail_h_left, tail_h_right, wing_left, wing_right,
            tail_h1_left, tail_h1_right)


# Запуск анимации
ani = FuncAnimation(fig, animate, frames=1000, interval=40, blit=True)
plt.tight_layout()
plt.show()
