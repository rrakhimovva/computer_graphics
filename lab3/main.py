import matplotlib.pyplot as plt


def bresenham_line(x0, y0, x1, y1):
    points = []

    dx = abs(x1 - x0)
    dy = abs(y1 - y0)

    sx = 1 if x1 > x0 else -1
    sy = 1 if y1 > y0 else -1

    # Если линия крутая — меняем оси
    steep = dy > dx
    if steep:
        x0, y0 = y0, x0
        x1, y1 = y1, x1
        dx, dy = dy, dx
        sx, sy = sy, sx

    f = 2 * dy - dx

    while x0 != x1:
        if steep:
            points.append((y0, x0))
        else:
            points.append((x0, y0))

        if f > 0:
            y0 += sy
            f -= 2 * dx

        f += 2 * dy
        x0 += sx

    if steep:
        points.append((y1, x1))
    else:
        points.append((x1, y1))

    return points


def bresenham_circle(cx, cy, r):
    points = []
    x = 0
    y = r
    d = 5 - 4 * r

    while x <= y:
        # все 8 симметричных точек
        points.extend([
            (cx + x, cy + y), (cx - x, cy + y),
            (cx + x, cy - y), (cx - x, cy - y),
            (cx + y, cy + x), (cx - y, cy + x),
            (cx + y, cy - x), (cx - y, cy - x)
        ])

        if d <= 0:
            d += 8 * x + 12
        else:
            d += 8 * (x - y) + 20
            y -= 1
        x += 1

    return points


def draw_grid(ax, xmin, xmax, ymin, ymax):
    for x in range(xmin, xmax + 1):
        ax.plot([x, x], [ymin, ymax], color='black', linewidth=0.5)
    for y in range(ymin, ymax + 1):
        ax.plot([xmin, xmax], [y, y], color='black', linewidth=0.5)


def draw_line(x0, y0, x1, y1):
    pixels = bresenham_line(x0, y0, x1, y1)

    print("Линия - пиксели:")
    for p in pixels:
        print(p)

    xs = [p[0] for p in pixels]
    ys = [p[1] for p in pixels]

    fig, ax = plt.subplots(figsize=(8, 8))

    margin = 5
    xmin = min(x0, x1) - margin
    xmax = max(x0, x1) + margin
    ymin = min(y0, y1) - margin
    ymax = max(y0, y1) + margin

    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)

    draw_grid(ax, xmin, xmax, ymin, ymax)
    ax.plot([x0, x1], [y0, y1], color='blue')
    ax.scatter(xs, ys, color='red')

    ax.set_aspect('equal')
    ax.axis('on')
    plt.show()


def draw_circle(cx, cy, r):
    pixels = bresenham_circle(cx, cy, r)

    print("Окружность - пиксели:")
    for p in pixels:
        print(p)

    xs = [p[0] for p in pixels]
    ys = [p[1] for p in pixels]

    fig, ax = plt.subplots(figsize=(8, 8))

    margin = r + 2
    xmin = cx - r - margin
    xmax = cx + r + margin
    ymin = cy - r - margin
    ymax = cy + r + margin

    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)

    # Сетка
    draw_grid(ax, xmin, xmax, ymin, ymax)

    # Окружность
    circle = plt.Circle((cx, cy), r, color='blue', fill=False)
    ax.add_patch(circle)

    # Пиксели
    ax.scatter(xs, ys, color='red')

    ax.set_aspect('equal')
    ax.axis('on')
    plt.show()


# draw_line(1, 5, 3, 10)

draw_line(-1, 1, -8, 2)

draw_circle(1, 1, 7)
