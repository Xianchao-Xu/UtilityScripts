# coding: utf-8
# author: xuxc


def create_space_point(x, y, z):
    """
    在SpaceClaim中创建空间点
    :param x: x坐标
    :param y: y坐标
    :param z: z坐标
    :return: None
    """
    point = Point.Create(x, y, z)
    SketchPoint.Create(point)
