import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon as MplPolygon
from matplotlib.widgets import Button


def draw_polygon_xor(width, height, points):
    xs = [x for x, y in points]
    ys = [y for x, y in points]

    center_x = (min(xs) + max(xs)) / 2
    center_y = (min(ys) + max(ys)) / 2

    shift_x = width / 2 - center_x
    shift_y = height / 2 - center_y

    points = [(x + shift_x, y + shift_y) for x, y in points]

    mask = np.zeros((height, width), dtype=np.int8)
    edges = []
    n = len(points)

    for i in range(n):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % n]

        if y1 == y2:
            continue
        if y1 > y2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1

        edges.append({'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2})

    fig, ax = plt.subplots(figsize=(10, 10))

    edge_id = 0

    def update_display():
        ax.clear()

        img_display = np.zeros((height, width, 3), dtype=np.uint8)
        img_display[mask == 0] = [255, 255, 255]
        img_display[mask == 1] = [192, 192, 192]
        ax.imshow(img_display)

        polygon = MplPolygon(points, fill=False, edgecolor='black', linewidth=2)
        ax.add_patch(polygon)

        for i in range(edge_id):
            e = edges[i]
            ax.plot([e['x1'], e['x2']], [e['y1'], e['y2']], 'r-', linewidth=2, alpha=0.5)

        if edge_id < len(edges):
            e = edges[edge_id]
            ax.plot([e['x1'], e['x2']], [e['y1'], e['y2']], 'g-', linewidth=3)
            ax.plot(e['x1'], e['y1'], 'go', markersize=8)
            ax.plot(e['x2'], e['y2'], 'go', markersize=8)

        ax.set_xlim(0, width + 20)
        ax.set_ylim(-200, height + 20)
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        fig.canvas.draw_idle()

    update_display()

    timer = fig.canvas.new_timer(interval=1500)

    def animate_step():
        nonlocal edge_id
        if edge_id < len(edges):
            edge = edges[edge_id]
            x1, y1, x2, y2 = edge['x1'], edge['y1'], edge['x2'], edge['y2']

            for y in range(int(y1), int(y2)):
                x = x1 + (x2 - x1) * (y - y1) / (y2 - y1)  # где ребро пересекает текущую строку
                x_int = int(round(x))
                for x_pixel in range(x_int, width):
                    if x_pixel < width and y < height:
                        mask[y, x_pixel] ^= 1

            edge_id += 1
            update_display()
        else:
            timer.stop()

    timer.add_callback(animate_step)

    ax_button = plt.axes([0.78, 0.78, 0.2, 0.07])
    btn = Button(ax_button, 'Запустить алгоритм')

    def on_click(event):
        if edge_id < len(edges):
            btn.color = '#dddddd'
            btn.set_active(False)
            timer.start()

    btn.on_clicked(on_click)

    plt.show()
    return mask


def load_polygon_from_file(filename):
    points = []
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            x, y = map(int, line.split())
            points.append((x, y))
    return points


width, height = 950, 950
polygon = load_polygon_from_file("points.txt")
draw_polygon_xor(width, height, polygon)
