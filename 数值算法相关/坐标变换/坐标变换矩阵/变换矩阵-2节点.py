# coding: utf-8
# author: xuxc
"""
    lx mx nx
T = ly my ny
    lz mz nz
其中，lx = cos(x, X), mx = cos(x, Y), nx = cos(x, Z)
     ly = cos(y, X), my = cos(y, Y), ny = cos(y, Z)
     lz = cos(z, X), mz = cos(z, Y), nz = cos(z, Z)
"""
from math import cos, pi, sin, sqrt
from random import random

import numpy as np


def cross(vec1: np.ndarray, vec2: np.ndarray) -> np.ndarray:
    return np.cross(vec1, vec2)


def rotate(vector: np.array, axis: np.array, rad: float):
    # 计算旋转轴上的单位向量
    axis_unit = axis / np.linalg.norm(axis)
    vector_unit = vector / np.linalg.norm(vector)

    # 点向轴投影
    vector_projection = np.dot(vector_unit, axis_unit) * axis_unit  # 投影后的向量，(V·K)K

    # 罗德里格公式
    term1 = vector_unit * cos(rad)
    term2 = vector_projection * (1 - cos(rad))
    term3 = cross(axis_unit, vector_unit) * sin(rad)
    result = term1 + term2 + term3

    return result


def trans_matrix(pnt1: np.array, pnt2: np.array, theta: float = 0):
    t33 = np.zeros((3, 3))
    v12 = pnt2 - pnt1
    dx = v12[0]
    dy = v12[1]
    dz = v12[2]
    length = sqrt(dx * dx + dy * dy + dz * dz)
    rad = theta * pi / 180.0
    cg = cos(rad)
    sg = sin(rad)
    den = length * sqrt(dx * dx + dz * dz)
    if den != 0.0:
        t33[0, 0] = dx / length
        t33[0, 1] = dy / length
        t33[0, 2] = dz / length
        t33[1, 0] = (-dx * dy * cg - length * dz * sg) / den
        t33[1, 1] = den * cg / (length * length)
        t33[1, 2] = (-dy * dz * cg + length * dx * sg) / den
        t33[2, 0] = (dx * dy * sg - length * dz * cg) / den
        t33[2, 1] = -den * sg / (length * length)
        t33[2, 2] = (dy * dz * sg + length * dx * cg) / den
    else:
        if dy > 0:
            t33[0, 0] = 0.0  # cos(x, X)
            t33[0, 1] = 1.0  # cos(x, Y)
            t33[0, 2] = 0.0  # cos(x, Z)
            t33[1, 0] = sg   # cos(y, X)
            t33[1, 1] = 0.0  # cos(y, Y)
            t33[1, 2] = cg   # cos(y, Z)
            t33[2, 0] = cg   # cos(z, X)
            t33[2, 1] = 0.0  # cos(z, Y)
            t33[2, 2] = -sg  # cos(z, Z)
        else:
            t33[0, 0] = 0.0   # cos(x, X)
            t33[0, 1] = -1.0  # cos(x, Y)
            t33[0, 2] = 0.0   # cos(x, Z)
            t33[1, 0] = sg    # cos(y, X)
            t33[1, 1] = 0.0   # cos(y, Y)
            t33[1, 2] = -cg   # cos(y, Z)
            t33[2, 0] = cg   # cos(z, X)
            t33[2, 1] = 0.0   # cos(z, Y)
            t33[2, 2] = sg   # cos(z, Z)
    return t33


def trans_matrix2(pnt1: np.array, pnt2: np.array, theta: float = 0):
    """
    轴线不平行于y轴时，可通过y轴与轴线（或者轴线在xz平面的投影）确定局部坐标系的z轴，再确定局部坐标系的y轴
    当轴线与y轴平行时，需考虑局部x轴与全局y轴同向还是反向。
    局部x轴与全局y轴同向时，可定义局部y轴与全局z轴同向、局部z轴与全局x轴同向。
    局部x轴与全局y轴反向时，可定义局部y轴与全局y轴反向、局部z轴与全局x轴反向。
    """
    global_x = np.array([1., 0., 0.])
    global_y = np.array([0., 1., 0.])
    global_z = np.array([0., 0., 1.])

    t33 = np.zeros((3, 3))
    v12 = pnt2 - pnt1
    dx = v12[0]
    dy = v12[1]
    dz = v12[2]
    length = sqrt(dx * dx + dy * dy + dz * dz)

    local_x = v12 / length
    projection = np.array([v12[0], 0, v12[2]])  # 局部坐标系在xz平面的投影
    length_projection = sqrt(dx * dx + dz * dz)  # 投影的长度
    if length_projection != 0.0:
        unit_projection = projection / length_projection  # 投影的单位向量
        local_z = cross(unit_projection, global_y)  # 投影与全局坐标系y轴叉乘，得到局部坐标系z轴
        local_y = cross(local_z, local_x)  # 局部坐标系z轴叉乘局部坐标系x轴，得到局部坐标系y轴
    else:
        if dy > 0:
            local_y = np.array([0.0, 0.0, 1.0])
            local_z = np.array([1.0, 0.0, 0.0])
        else:
            local_y = np.array([0.0, 0.0, -1.0])
            local_z = np.array([1.0, 0.0, 0.0])

    if theta != 0.0:
        rad = pi / 180. * theta
        local_y = rotate(local_y, local_x, rad)
        local_z = rotate(local_z, local_x, rad)
    t33[0, 0] = local_x.dot(global_x)
    t33[0, 1] = local_x.dot(global_y)
    t33[0, 2] = local_x.dot(global_z)
    t33[1, 0] = local_y.dot(global_x)
    t33[1, 1] = local_y.dot(global_y)
    t33[1, 2] = local_y.dot(global_z)
    t33[2, 0] = local_z.dot(global_x)
    t33[2, 1] = local_z.dot(global_y)
    t33[2, 2] = local_z.dot(global_z)
    return t33


if __name__ == '__main__':
    x1 = random()
    y1 = random()
    z1 = random()
    x2 = random()
    y2 = random()
    z2 = random()
    angle = random() * 180
    p1 = np.array([x1, y1, z1])
    p2 = np.array([x2, y2, z2])
    t1 = trans_matrix(p1, p2, angle)
    t2 = trans_matrix2(p1, p2, angle)
    print(t1 - t2)
    t1 = trans_matrix(np.array([0, 0, 0]), np.array([0, 1, 0]), angle)
    t2 = trans_matrix2(np.array([0, 0, 0]), np.array([0, 1, 0]), angle)
    print(t1 - t2)
    t1 = trans_matrix(np.array([0, 0, 0]), np.array([0, -1, 0]), angle)
    t2 = trans_matrix2(np.array([0, 0, 0]), np.array([0, -1, 0]), angle)
    print(t1 - t2)
