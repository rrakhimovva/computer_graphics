import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk, simpledialog
import math


# Класс для работы с матричными преобразованиями
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
    def multiply_matrices(A, B):
        """Умножение двух матриц 3x3"""
        result = [[0, 0, 0] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    result[i][j] += A[i][k] * B[k][j]
        return result

    @staticmethod
    def create_translation_matrix(dx, dy):
        """Матрица сдвига 3x3"""
        return [
            [1, 0, dx],
            [0, 1, dy],
            [0, 0, 1]
        ]

    @staticmethod
    def create_reflection_ox_matrix():
        """Отражение относительно оси OX"""
        return [
            [1, 0, 0],
            [0, -1, 0],
            [0, 0, 1]
        ]

    @staticmethod
    def create_reflection_oy_matrix():
        """Отражение относительно оси OY"""
        return [
            [-1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
        ]

    @staticmethod
    def create_reflection_yx_matrix():
        """Отражение относительно прямой Y=X"""
        return [
            [0, 1, 0],
            [1, 0, 0],
            [0, 0, 1]
        ]

    @staticmethod
    def create_scaling_matrix(sx, sy):
        """Матрица масштабирования"""
        return [
            [sx, 0, 0],
            [0, sy, 0],
            [0, 0, 1]
        ]

    @staticmethod
    def create_rotation_matrix(angle_degrees):
        """Матрица поворота на угол относительно центра координат"""
        angle_rad = math.radians(angle_degrees)
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)
        return [
            [cos_a, -sin_a, 0],
            [sin_a, cos_a, 0],
            [0, 0, 1]
        ]

    @staticmethod
    def create_rotation_around_point_matrix(angle_degrees, cx, cy):
        """Матрица поворота относительно произвольной точки (cx, cy)"""
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


# Класс фигуры (звезды)
class StarFigure:
    def __init__(self):
        self.original_big_triangle = [
            [-4, 4, 1],
            [4, 4, 1],
            [0, 0, 1]
        ]

        self.original_small_triangle1 = [
            [1.6, 1.6, 1],
            [0, 0, 1],
            [8 / 3, -8 / 3, 1]
        ]

        self.original_small_triangle2 = [
            [-1.6, 1.6, 1],
            [0, 0, 1],
            [-8 / 3, -8 / 3, 1]
        ]

        self.original_diamond = [
            [0, 8, 1],
            [1, 4, 1],
            [0, 0, 1],
            [-1, 4, 1]
        ]

        # Текущие матрицы (копия оригиналов)
        self.reset()

    def reset(self):
        """Сброс к исходной позиции"""
        self.big_triangle = [v.copy() for v in self.original_big_triangle]
        self.small_triangle1 = [v.copy() for v in self.original_small_triangle1]
        self.small_triangle2 = [v.copy() for v in self.original_small_triangle2]
        self.diamond = [v.copy() for v in self.original_diamond]

    def apply_transform(self, transform_matrix):
        """Применение преобразования ко всем частям фигуры"""
        self.big_triangle = MatrixTransform.apply_transform(self.big_triangle, transform_matrix)
        self.small_triangle1 = MatrixTransform.apply_transform(self.small_triangle1, transform_matrix)
        self.small_triangle2 = MatrixTransform.apply_transform(self.small_triangle2, transform_matrix)
        self.diamond = MatrixTransform.apply_transform(self.diamond, transform_matrix)

    def get_all_vertices(self):
        """Получить все вершины для определения границ"""
        all_vertices = []
        for vertices in [self.big_triangle, self.small_triangle1,
                         self.small_triangle2, self.diamond]:
            all_vertices.extend([[v[0], v[1]] for v in vertices])
        return all_vertices


# Класс приложения
class TransformApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1000x800")

        # Создаем фигуру
        self.star = StarFigure()

        # Создаем интерфейс
        self.setup_ui()

        # Рисуем начальную фигуру
        self.redraw()

    def setup_ui(self):
        """Создание элементов интерфейса"""
        # Главный фрейм
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Фрейм для графика
        plot_frame = ttk.Frame(main_frame)
        plot_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Создаем фигуру matplotlib
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Фрейм для кнопок
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

        row1 = ttk.Frame(buttons_frame)
        row1.pack(fill=tk.X, pady=2)

        ttk.Button(row1, text="Перенос по OX",
                   command=self.translate_ox).pack(side=tk.LEFT, padx=2)
        ttk.Button(row1, text="Перенос по OY",
                   command=self.translate_oy).pack(side=tk.LEFT, padx=2)
        ttk.Button(row1, text="Отражение OX",
                   command=self.reflect_ox).pack(side=tk.LEFT, padx=2)
        ttk.Button(row1, text="Отражение OY",
                   command=self.reflect_oy).pack(side=tk.LEFT, padx=2)

        row2 = ttk.Frame(buttons_frame)
        row2.pack(fill=tk.X, pady=2)

        ttk.Button(row2, text="Отражение Y=X",
                   command=self.reflect_yx).pack(side=tk.LEFT, padx=2)
        ttk.Button(row2, text="Масштабирование",
                   command=self.scale).pack(side=tk.LEFT, padx=2)
        ttk.Button(row2, text="Поворот вокруг (0,0)",
                   command=self.rotate_origin).pack(side=tk.LEFT, padx=2)
        ttk.Button(row2, text="Поворот вокруг точки",
                   command=self.rotate_around_point).pack(side=tk.LEFT, padx=2)

        row3 = ttk.Frame(buttons_frame)
        row3.pack(fill=tk.X, pady=2)

        ttk.Button(row3, text="Сброс",
                   command=self.reset).pack(side=tk.LEFT, padx=2)

    def redraw(self):
        """Отрисовка фигуры"""
        self.ax.clear()

        # Функция для извлечения координат
        def get_xy(vertices):
            return [[v[0], v[1]] for v in vertices]

        # Рисуем большой треугольник
        self.ax.add_patch(patches.Polygon(
            get_xy(self.star.big_triangle),
            closed=True, fill=None, edgecolor='black', linewidth=2.5
        ))

        # Рисуем маленькие треугольники
        self.ax.add_patch(patches.Polygon(
            get_xy(self.star.small_triangle1),
            closed=True, fill=None, edgecolor='black', linewidth=2.5
        ))

        self.ax.add_patch(patches.Polygon(
            get_xy(self.star.small_triangle2),
            closed=True, fill=None, edgecolor='black', linewidth=2.5
        ))

        # Рисуем ромб
        self.ax.add_patch(patches.Polygon(
            get_xy(self.star.diamond),
            closed=True, fill=None, edgecolor='black', linewidth=2.5
        ))

        # Линия внутри ромба
        line_points = [self.star.diamond[0][:2], self.star.diamond[2][:2]]
        self.ax.plot([line_points[0][0], line_points[1][0]],
                     [line_points[0][1], line_points[1][1]],
                     'black', linewidth=3)

        # Определяем границы для отображения
        all_vertices = self.star.get_all_vertices()
        xs = [v[0] for v in all_vertices]
        ys = [v[1] for v in all_vertices]

        # Добавляем запас 20%
        x_min, x_max = min(xs), max(xs)
        y_min, y_max = min(ys), max(ys)
        x_range = max(abs(x_min), abs(x_max)) * 1.2
        y_range = max(abs(y_min), abs(y_max)) * 1.2

        # Начало координат всегда в центре
        self.ax.set_xlim(-x_range, x_range)
        self.ax.set_ylim(-y_range, y_range)
        self.ax.set_aspect('equal')
        self.ax.grid(True, alpha=0.3)

        # Рисуем оси через центр
        self.ax.axhline(y=0, color='gray', linestyle='-', linewidth=0.5)
        self.ax.axvline(x=0, color='gray', linestyle='-', linewidth=0.5)

        # Отмечаем центр
        self.ax.scatter(0, 0, color='red', s=30, zorder=5)

        self.canvas.draw()


    def translate_ox(self):
        """Перенос вдоль оси OX"""
        dx = simpledialog.askfloat("Перенос по OX",
                                   "Введите величину сдвига по X:",
                                   initialvalue=1.0)
        if dx is not None:
            matrix = MatrixTransform.create_translation_matrix(dx, 0)
            self.star.apply_transform(matrix)
            self.redraw()

    def translate_oy(self):
        """Перенос вдоль оси OY"""
        dy = simpledialog.askfloat("Перенос по OY",
                                   "Введите величину сдвига по Y:",
                                   initialvalue=1.0)
        if dy is not None:
            matrix = MatrixTransform.create_translation_matrix(0, dy)
            self.star.apply_transform(matrix)
            self.redraw()

    def reflect_ox(self):
        """Отражение относительно оси OX"""
        matrix = MatrixTransform.create_reflection_ox_matrix()
        self.star.apply_transform(matrix)
        self.redraw()

    def reflect_oy(self):
        """Отражение относительно оси OY"""
        matrix = MatrixTransform.create_reflection_oy_matrix()
        self.star.apply_transform(matrix)
        self.redraw()

    def reflect_yx(self):
        """Отражение относительно прямой Y=X"""
        matrix = MatrixTransform.create_reflection_yx_matrix()
        self.star.apply_transform(matrix)
        self.redraw()

    def scale(self):
        """Масштабирование независимо по осям"""
        sx = simpledialog.askfloat("Масштаб по X",
                                   "Введите коэффициент масштаба по X:",
                                   initialvalue=1.5)
        if sx is None:
            return
        sy = simpledialog.askfloat("Масштаб по Y",
                                   "Введите коэффициент масштаба по Y:",
                                   initialvalue=1.5)
        if sy is not None:
            matrix = MatrixTransform.create_scaling_matrix(sx, sy)
            self.star.apply_transform(matrix)
            self.redraw()

    def rotate_origin(self):
        """Поворот относительно центра координат"""
        angle = simpledialog.askfloat("Поворот",
                                      "Введите угол поворота (градусы):",
                                      initialvalue=45)
        if angle is not None:
            matrix = MatrixTransform.create_rotation_matrix(angle)
            self.star.apply_transform(matrix)
            self.redraw()

    def rotate_around_point(self):
        """Поворот относительно произвольной точки"""
        cx = simpledialog.askfloat("Координата X",
                                   "Введите X координату центра поворота:",
                                   initialvalue=0)
        if cx is None:
            return
        cy = simpledialog.askfloat("Координата Y",
                                   "Введите Y координату центра поворота:",
                                   initialvalue=0)
        if cy is None:
            return
        angle = simpledialog.askfloat("Угол",
                                      "Введите угол поворота (градусы):",
                                      initialvalue=45)
        if angle is not None:
            matrix = MatrixTransform.create_rotation_around_point_matrix(angle, cx, cy)
            self.star.apply_transform(matrix)
            self.redraw()

    def reset(self):
        """Сброс к исходной позиции"""
        self.star.reset()
        self.redraw()

# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = TransformApp(root)
    root.mainloop()
