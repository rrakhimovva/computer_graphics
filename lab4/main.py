import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Button, RadioButtons
from matplotlib.patches import Polygon

INSIDE = 0
LEFT = 1
RIGHT = 2
BOTTOM = 4
TOP = 8
EPS = 0.0001


class Clipping:
    def __init__(self):
        self.fig = plt.figure(figsize=(9, 9))
        self.fig.canvas.manager.set_window_title('Clipping line')
        self.ax = self.fig.add_subplot()
        self.__initAxes()
        self.fig.subplots_adjust(bottom=0.2)
        self.polygon_file = 'polygon.txt'
        self.__initPolygon()
        self.line_file = 'line.txt'
        self.__initLine()
        self.__initUI()

        # изменить сетку
    def __initAxes(self):
        self.ax.spines['left'].set_position('center')
        self.ax.spines['bottom'].set_position('center')
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.set(
            xlim=(-10, 10),
            xticks=np.arange(-10, 10, 1),
            ylim=(-10, 10),
            yticks=np.arange(-10, 10, 1)
        )
        self.ax.grid(True)

    def __initUI(self):
        self.ax.set_title('Before clipping')
        self.__initClippingButton()
        if self.rectangle:
            self.__initChoosingLineType()

    def __initClippingButton(self):
        self.b_clip_axes = self.fig.add_axes([0.65, 0.05, 0.15, 0.05])
        self.b_clip = Button(
            self.b_clip_axes,
            'Clip',
            hovercolor='white'
        )
        self.b_clip.on_clicked(self.__clip)

    def __initChoosingLineType(self):
        clipping_line_type = ['Cyrus-Beck', 'Cohen-Sutherland', 'Midle-point']
        self.choose_clipping_line_type_axes = self.fig.add_axes(
            [0.4, 0.05, 0.2, 0.08],
            facecolor='#d9d9d9'
        )
        self.rbs_clipping_line_type = RadioButtons(
            self.choose_clipping_line_type_axes,
            clipping_line_type,
            radio_props={'s': [64, 64, 64]},
            activecolor='black',
        )
        self.rbs_clipping_line_type.on_clicked(self.__choosingAlgorithm)

        self.current_clipping_line_type = clipping_line_type[0]

    def __initPolygon(self):
        self.rectangle = False
        self.polygon_coords = np.genfromtxt(
            self.polygon_file,
            delimiter=' '
        )
        # Многоугольник
        if self.polygon_coords.size / 2 > 2:
            self.rectangle = False
        elif self.polygon_coords.size / 2 < 2:
            raise ValueError("Invalid input data size")
        # Прямоугольник
        else:
            self.rectangle = True
            self.min_x, self.min_y = self.polygon_coords[0]
            self.max_x, self.max_y = self.polygon_coords[1]

    def __initLine(self):
        self.const_line_coords = np.genfromtxt(self.line_file)

    def run(self):
        self.__redrawScene()
        plt.show()

    def __drawPolygon(self):
        if self.rectangle and self.polygon_coords.size == 4:
            self.polygon_coords = np.array([
                [
                    self.polygon_coords[0][0],
                    self.polygon_coords[0][1]
                ],
                [
                    self.polygon_coords[1][0],
                    self.polygon_coords[0][1]
                ],
                [
                    self.polygon_coords[1][0],
                    self.polygon_coords[1][1]
                ],
                [
                    self.polygon_coords[0][0],
                    self.polygon_coords[1][1]
                ]
            ])
        points = np.array(list(map(lambda x: x[:2], self.polygon_coords)))
        polygon = Polygon(
            points,
            fc='none',
            ec='black',
            closed=True,
            lw=2
        )
        self.ax.add_patch(polygon)

    def __drawAnyLine(self, line_coords, color='black'):
        x, y = np.hsplit(line_coords, 2)
        line = plt.Line2D(
            x,
            y,
            lw=2,
            color=color
        )
        self.ax.add_line(line)

    def __redrawScene(self):
        self.__drawPolygon()
        self.__drawAnyLine(self.const_line_coords)

        # точки концов линии
        self.ax.plot(self.const_line_coords[0][0],
                     self.const_line_coords[0][1],
                     'go')

        self.ax.plot(self.const_line_coords[1][0],
                     self.const_line_coords[1][1],
                     'go')

    def __choosingAlgorithm(self, label_name):
        self.ax.clear()
        self.__initAxes()
        self.ax.set_title('Before clipping')

        if label_name == 'Cyrus-Beck':
            self.current_clipping_line_type = 'Cyrus-Beck'
        elif label_name == 'Cohen-Sutherland':
            self.current_clipping_line_type = 'Cohen-Sutherland'
        elif label_name == 'Midle-point':
            self.current_clipping_line_type = 'Midle-point'

        self.__redrawScene()

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def __drawFigures(self):
        self.__drawPolygon()
        self.__drawAnyLine(self.const_line_coords)

    def __clip(self, event):
        self.ax.set_title('After clipping')
        if self.rectangle:
            if self.current_clipping_line_type == 'Cyrus-Beck':
                self.__clipCyrusBeck()
            elif self.current_clipping_line_type == 'Cohen-Sutherland':
                self.__clipCohenSutherland()
            elif self.current_clipping_line_type == 'Midle-point':
                self.__clipMidlePoint()
        else:
            self.__clipCyrusBeck()

    def __clipCyrusBeck(self):
        self.clipped_cyrus_beck_line = self.__cyrusBeck()
        if self.clipped_cyrus_beck_line is None:
            self.fig.canvas.draw()
            self.fig.canvas.flush_events()

        self.__drawAnyLine(self.clipped_cyrus_beck_line, '#7fffd4')

        # Рисуем потеницальные точки входа и выхода
        for point in self.intersections_in:
            self.ax.plot(point[0], point[1], 'mo')
        for point in self.intersections_out:
            self.ax.plot(point[0], point[1], 'bo')

        self.ax.plot(
            self.clipped_cyrus_beck_line[:, 0],
            self.clipped_cyrus_beck_line[:, 1],
            'ro'
        )

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def __cyrusBeck(self):
        num_vert = int(self.polygon_coords.size / 2)
        # вектор направление отрезка от начальной до конечной
        P1_P0 = np.array([
            self.const_line_coords[1][0] - self.const_line_coords[0][0],
            self.const_line_coords[1][1] - self.const_line_coords[0][1]
        ])
        # векторы нормали для каждой границы
        normal = np.array([[
            self.polygon_coords[i][1] -
            self.polygon_coords[(i + 1) % num_vert][1],
            self.polygon_coords[(i + 1) % num_vert][0] -
            self.polygon_coords[i][0]
        ] for i in range(num_vert)])
        # векторы от начальной точки до каждой из вершин полигона
        P0_PEi = np.array([[
            self.polygon_coords[i][0] - self.const_line_coords[0][0],
            self.polygon_coords[i][1] - self.const_line_coords[0][1]
        ] for i in range(num_vert)])

        # где находится начальная точка отрезка относительно нормали
        numerator = np.array([np.dot(normal[i], P0_PEi[i])
                              for i in range(num_vert)])
        # как отрезок направлен относительно границы
        denominator = np.array([np.dot(normal[i], P1_P0)
                                for i in range(num_vert)])

        # параметр пересечения с каждой границей
        t = np.array([numerator[i] / denominator[i]
                      if denominator[i] != 0 else 0 for i in range(num_vert)])

        # определение точек входа и выхода
        Te = np.array([t[i] for i in range(num_vert) if denominator[i] > 0])
        Tl = np.array([t[i] for i in range(num_vert) if denominator[i] < 0])

        # координаты точек, где отрезок входит в многоугольник
        self.intersections_in = np.array([
            (
                self.const_line_coords[0][0] + P1_P0[0] * Te[i],
                self.const_line_coords[0][1] + P1_P0[1] * Te[i]
            ) for i in range(Te.size)
        ])
        # координаты точек, где отрезок выходит из многоугольника
        self.intersections_out = np.array([
            (
                self.const_line_coords[0][0] + P1_P0[0] * Tl[i],
                self.const_line_coords[0][1] + P1_P0[1] * Tl[i]
            ) for i in range(Tl.size)
        ])

        # проверка на границы
        for i in range(num_vert):
            if denominator[i] == 0:
                if numerator[i] > 0:
                    return None

        Te = np.array([*Te, 0.0])
        Tl = np.array([*Tl, 1.0])

        temp = np.array([max(Te), min(Tl)])

        if temp[0] > temp[1]:
            return None

        # возвращение обрезанного отрезка
        self.clipped_cyrus_beck_line = np.array([
            [
                self.const_line_coords[0][0] + P1_P0[0] * temp[0],
                self.const_line_coords[0][1] + P1_P0[1] * temp[0]
            ],
            [
                self.const_line_coords[0][0] + P1_P0[0] * temp[1],
                self.const_line_coords[0][1] + P1_P0[1] * temp[1]
            ]
        ])

        return self.clipped_cyrus_beck_line

    def __clipCohenSutherland(self):
        self.clipped_cohen_sutherland_line = self.__cohenSutherland()
        if self.clipped_cohen_sutherland_line is not None:
            self.__drawAnyLine(self.clipped_cohen_sutherland_line, '#7fffd4')

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def __calculateCode(self, point):
        code = INSIDE
        if point[0] < self.min_x:
            code |= LEFT
        if point[0] > self.max_x:
            code |= RIGHT
        if point[1] < self.min_y:
            code |= BOTTOM
        if point[1] > self.max_y:
            code |= TOP
        return code

    def __cohenSutherland(self):
        line = np.copy(self.const_line_coords)
        code0 = self.__calculateCode(line[0])
        code1 = self.__calculateCode(line[1])
        accept = False

        while True:
            if code0 == 0 and code1 == 0:
                accept = True
                break
            elif (code0 & code1) != 0:
                break
            else:
                x = 0.0
                y = 0.0
                if code0 != 0:
                    code_out = code0
                else:
                    code_out = code1
                if code_out & TOP:
                    x = line[0][0] + (
                            (line[1][0] - line[0][0])
                            *
                            (self.max_y - line[0][1])
                            /
                            (line[1][1] - line[0][1])
                    )
                    y = self.max_y
                elif code_out & BOTTOM:
                    x = line[0][0] + (
                            (line[1][0] - line[0][0])
                            *
                            (self.min_y - line[0][1])
                            /
                            (line[1][1] - line[0][1])
                    )
                    y = self.min_y
                elif code_out & RIGHT:
                    y = line[0][1] + (
                            (line[1][1] - line[0][1])
                            *
                            (self.max_x - line[0][0])
                            /
                            (line[1][0] - line[0][0])
                    )
                    x = self.max_x
                elif code_out & LEFT:
                    y = line[0][1] + (
                            (line[1][1] - line[0][1])
                            *
                            (self.min_x - line[0][0])
                            /
                            (line[1][0] - line[0][0])
                    )
                    x = self.min_x

                self.ax.plot(x, y, 'ro')

                if code_out == code0:
                    line[0][0] = x
                    line[0][1] = y
                    code0 = self.__calculateCode(line[0])
                else:
                    line[1][0] = x
                    line[1][1] = y
                    code1 = self.__calculateCode(line[1])

        if accept:
            self.ax.plot(line[0][0], line[0][1], 'ro')
            self.ax.plot(line[1][0], line[1][1], 'ro')
            return line

    def __clipMidlePoint(self):
        self.__midlePoint(self.const_line_coords)

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def __midlePoint(self, prev_line):
        line = np.copy(prev_line)
        code0 = self.__calculateCode(line[0])
        code1 = self.__calculateCode(line[1])
        # Если длина отрезка меньше пикселя, то не рассматриваем его
        if np.sqrt(
                np.square(line[0][0] - line[1][0])
                +
                np.square(line[0][1] - line[1][1])
        ) < EPS:
            return

        # Если отрезок целиком внутри области, то отрисовываем его
        if code0 == 0 and code1 == 0:
            self.ax.plot((line[0][0], line[1][0]), (line[0][1], line[1][1]), 'ro')
            self.__drawAnyLine(line, '#7fffd4')
            return

        # Если отрезок целиком вне области, то не рассматриваем его
        if (code0 & code1) != 0:
            return

        A = line[0]
        B = line[1]
        new_x = ((A[0] + B[0]) / 2)
        new_y = ((A[1] + B[1]) / 2)

        # Делим отрезок на две части и используем алгоритм для этих частей
        self.__midlePoint(np.array([
            A,
            [
                new_x,
                new_y
            ]
        ]))
        self.__midlePoint(np.array([
            [
                new_x,
                new_y
            ],
            B
        ]))

app = Clipping()
app.run()
