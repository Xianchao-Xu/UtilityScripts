# coding: utf-8
# author: xuxc
from math import sin, cos, pi

import numpy as np
import matplotlib.pyplot as plt


def rotate(point, point1, point2, rad, show=False):
    """
    点绕任意轴线旋转一定弧度后的坐标
    向量V绕单位向量K旋转θ弧度后得到向量V_r，V_r可由罗德里格旋转公式表示：
        V_r = Vcosθ + (V·K)K(1-cosθ) + K×Vsinθ
    :param point: 需要旋转的点
    :param point1: 旋转轴上的点1
    :param point2: 旋转轴上的点2
    :param rad: 旋转的弧度
    :param show: 是否显示示意图
    :return: 旋转后的点
    """
    # 将点用NumPy数组表示
    point = np.array(point, dtype=float)
    point1 = np.array(point1, dtype=float)
    point2 = np.array(point2, dtype=float)

    # 计算旋转轴上的单位向量
    axis = point2 - point1
    axis_unit = axis / np.linalg.norm(axis)

    # 点向轴投影
    vector_origin = point - point1
    vector_projection = np.dot(vector_origin, axis_unit) * axis_unit  # 投影后的向量，(V·K)K
    point_projection = point1 + vector_projection

    # 罗德里格公式
    term1 = vector_origin * cos(rad)
    term2 = vector_projection * (1 - cos(rad))
    term3 = np.cross(axis_unit, vector_origin) * sin(rad)
    vector_rotate = term1 + term2 + term3
    new_point = point1 + vector_rotate

    if show:
        points_to_show = dict()
        points_to_show['P'] = point
        points_to_show['P1'] = point1
        points_to_show['P2'] = point2
        points_to_show['P_{projection}'] = point_projection
        points_to_show['P_{rotate}'] = new_point

        arrows_to_show = dict()
        arrows_to_show[r'V_{axis}'] = [point1, axis]
        arrows_to_show[r'V_{origin}'] = [point1, vector_origin]
        arrows_to_show[r'V_{rotate}'] = [point1, vector_rotate]

        show_picture(points_to_show, arrows_to_show)
    return new_point


def rotate_xyz(points, axis, degree):
    """
    返回点绕轴旋转一定角度后的值。
    旋转方向由右手法则确定：
        大拇指指向坐标轴方向，旋转方向顺着另外四根手指头为正，反之为负

    :param points: 由x、y、z坐标构成的列表
    :param axis: 绕哪一个轴旋转
    :param degree: 旋转的度数
    :return: 旋转后的坐标
    """
    rad = degree * pi / 180.
    if axis == 'x':
        x = points[0]
        y = points[1] * cos(rad) - points[2] * sin(rad)
        z = points[1] * sin(rad) + points[2] * cos(rad)
    elif axis == 'y':
        z = points[2] * cos(rad) - points[0] * sin(rad)
        y = points[1]
        x = points[2] * sin(rad) + points[0] * cos(rad)
    elif axis == 'z':
        x = points[0] * cos(rad) - points[1] * sin(rad)
        y = points[0] * sin(rad) + points[1] * cos(rad)
        z = points[2]
    else:
        print('只支持绕坐标轴旋转')
        x, y, z = points
    return x, y, z


def show_picture(points, arrows):
    fig = plt.figure(figsize=(9, 9))
    ax = fig.add_subplot(111, projection='3d', proj_type='ortho')
    # ax.set_axis_off()  # 隐藏坐标轴
    ax.grid(False)  # 隐藏网格线

    for point_name in points:
        point = points[point_name]
        x, y, z = point
        ax.scatter(x, y, z, c='r', marker='o')
        ax.text(x, y, z, r'${}$'.format(point_name))

    for arrow_name in arrows:
        arrow = arrows[arrow_name]
        x, y, z = arrow[0]  # 箭头位置
        dx, dy, dz = arrow[1]  # 箭头大小
        ax.quiver(x, y, z, dx, dy, dz, colors='g', arrow_length_ratio=0.1)
        ax.text(x+dx/2, y+dy/2, z+dz/2, r'${}$'.format(arrow_name))

    l_min = 1.e20
    l_max = -1.e20
    for dim in 'xyz':
        lim_min, lim_max = getattr(ax, 'get_{}lim'.format(dim))()
        l_min = min(l_min, lim_min)
        l_max = max(l_max, lim_max)
    for dim in 'xyz':
        getattr(ax, 'set_{}lim'.format(dim))([l_min, l_max])
    plt.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
    plt.show()


if __name__ == '__main__':
    deg = 45
    r = deg * pi / 180.
    p = [1, 2, 3]
    p1 = [0, 5, 2]
    p2 = [1, 5, 5]
    p_new = rotate(p, p1, p2, r, show=True)
    print(p_new)
