import matplotlib.pyplot as plt
from matplotlib.widgets import Button


class MCH:
    def __init__(self):
        self.fig = plt.figure(figsize=(9, 9))
        self.ax = self.fig.add_subplot()
        self.__initAxes()
        self.fig.subplots_adjust(bottom=0.05)
        self.__initUI()
        self.path = 'points.txt'
        self.points = []
        self.__load()

    def __initAxes(self):
        self.ax.spines['left'].set_visible(True)
        self.ax.spines['bottom'].set_visible(True)
        self.ax.spines['top'].set_visible(True)
        self.ax.spines['right'].set_visible(True)
        self.ax.set(
            xlim=(-40, 100),
            xticks=[],
            ylim=(-40, 100),
            yticks=[]
        )
        self.ax.grid(False)

    def __initUI(self):
        self.__initStartButton()

    def __initStartButton(self):
        self.start_axes = self.fig.add_axes([0.45, 0.9, 0.15, 0.05])
        self.b_start = Button(
            self.start_axes,
            'Start',
            hovercolor='white'
        )
        self.b_start.label.set_fontsize(14)
        self.b_start.on_clicked(self.__jarvis)

    def __load(self):
        with open(self.path, 'r') as points:
            for p in points:
                row = p.split(' ')
                self.points.append([int(row[0]), int(row[1])])
        self.ax.scatter(
            [p[0] for p in self.points],
            [p[1] for p in self.points],
            color='blue'
        )
        self.fig.canvas.draw()

    def run(self):
        plt.show()

    def __rotate(self, A, B, C):
        return (B[0]-A[0])*(C[1]-B[1]) - (B[1]-A[1])*(C[0]-B[0])

    def __jarvis(self, event):
        n = len(self.points)
        P = [i for i in range(n)]
        for i in range(1, n):
            if self.points[P[i]][0] < self.points[P[0]][0]:
                P[i], P[0] = P[0], P[i]
        H = [P[0]]
        del P[0]
        P.append(H[0])
        step = 0
        self.ax.plot(
            *self.points[H[0]],
            color='red',
            marker='o'
        )
        while True:
            right = 0
            for i in range(1, len(P)):
                self.ax.plot(
                    [self.points[H[-1]][0], self.points[P[i]][0]],
                    [self.points[H[-1]][1], self.points[P[i]][1]],
                    color='green'
                )
                if self.__rotate(self.points[H[-1]], self.points[P[right]], self.points[P[i]]) < 0:
                    right = i
                plt.pause(0.07)

                self.ax.clear()
                self.__initAxes()
                self.ax.scatter(
                    [p[0] for p in self.points],
                    [p[1] for p in self.points],
                    color='blue'
                )
                self.ax.plot(
                    [self.points[p][0] for p in H],
                    [self.points[p][1] for p in H],
                    color='red',
                    marker='o'
                )
                self.ax.plot(
                    [self.points[H[-1]][0], self.points[P[right]][0]],
                    [self.points[H[-1]][1], self.points[P[right]][1]],
                    color='black'
                )
            if P[right] == H[0]:
                break
            else:
                H.append(P[right])
                del P[right]
            step += 1
            plt.pause(0.07)
            self.fig.canvas.draw()
        self.ax.plot([self.points[H[step % len(H)]][0], self.points[H[(step+1) % len(H)]][0]],
                     [self.points[H[step % len(H)]][1], self.points[H[(step+1) % len(H)]][1]], color='red', marker='o')
        self.fig.canvas.draw()
        return H

app = MCH()
app.run()
