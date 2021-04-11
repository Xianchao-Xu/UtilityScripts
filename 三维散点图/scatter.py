# coding: utf-8
# author: xuxc
import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure(figsize=(6, 6))
ax = fig.add_subplot(111, projection='3d', proj_type='ortho')
ax.set_axis_off()  # 隐藏坐标轴
# ax.grid(False)  # 隐藏网格线

# 绘制坐标系箭头
ax.quiver([0], [0], [0], [1], [0], [0], colors='r', length=1.0)
ax.quiver([0], [0], [0], [0], [1], [0], colors='g', length=1.0)
ax.quiver([0], [0], [0], [0], [0], [1], colors='b', length=1.0)
ax.text(0.0, 0.0, -0.1, r'$o$')
ax.text(1.1, 0, 0, r'$x$')
ax.text(0, 1.1, 0, r'$y$')
ax.text(0, 0, 1.1, r'$z$')

max_lim = -1.e20
min_lim = 1.e20

scatters = np.loadtxt('scatter_data.dat', skiprows=0, usecols=(1, 2, 3))
num_points = np.shape(scatters)[0]
for i in range(num_points):
    x, y, z = scatters[i]
    min_lim = np.min([min_lim, x, y, z])
    max_lim = np.max([max_lim, x, y, z])
    ax.scatter(xs=x, ys=y, zs=z, c='r', marker='o')

ax.set_xlim([min_lim, max_lim])
ax.set_ylim([min_lim, max_lim])
ax.set_zlim([min_lim, max_lim])

plt.subplots_adjust(left=0.0, right=1., top=1., bottom=0.0)
# plt.savefig('scatter.png')
plt.show()
