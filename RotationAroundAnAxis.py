# coding: utf-8
# author: xuxc
from math import sin, cos, pi


def rotate(points, axis, degree):
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


if __name__ == '__main__':
    print(rotate([10, 10, 40], 'y', 50))
