# coding: utf-8
# author: xuxc
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig = plt.figure(figsize=(9, 6))
ax = fig.add_subplot(111)

x = np.arange(0, 2*np.pi, 0.01)
line, = ax.plot(x, np.sin(x))


def animate(i):
    x = line.get_xdata()
    x = x * 1.001
    line.set_xdata(x)
    line.set_ydata(np.sin(x))  # update the data.
    ax.set_xlim(min(x), max(x))
    return line,


# blit=False时，xlim才会更新
ani = animation.FuncAnimation(fig, animate, interval=20, blit=False, save_count=500)

# ani.save("movie.mp4")

plt.show()
