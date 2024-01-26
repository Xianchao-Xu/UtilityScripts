#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np


def cross(vec1: np.ndarray, vec2: np.ndarray) -> np.ndarray:
    return np.cross(vec1, vec2)


def coordinate_translate(point1: np.array, point2: np.array, point3: np.array, point: np.array) -> np.array:
    """
    计算点在局部坐标系下的坐标
    :param point1: 局部坐标系原点
    :param point2: 局部坐标系x轴上的1点
    :param point3: 局部坐标系xy平面上的1点
    :param point: 需要计算坐标的点
    :return: 点在局部坐标系下的坐标
    """
    p12 = point2 - point1
    p13 = point3 - point1
    x_local = p12 / np.linalg.norm(p12)  # 局部坐标系x轴
    vector_z = cross(p12, p13)
    z_local = vector_z / np.linalg.norm(vector_z)  # 局部坐标系z轴
    y_local = cross(z_local, x_local)  # 局部坐标系y轴
    vector = point - p1
    x = vector.dot(x_local)
    y = vector.dot(y_local)
    z = vector.dot(z_local)
    return np.array([x, y, z])


if __name__ == '__main__':
    p1 = np.array([0.5, 0., 0.0])
    p2 = np.array([0.5, 1.0, 0.0])
    p3 = np.array([1.0, 0.0, 0.0])
    p = np.array([0.0, 1.0, 0.0])
    print(coordinate_translate(p1, p2, p3, p))

    p1 = np.array([0.5, 0.5, 0.0])
    p2 = np.array([0.5, 1.0, 0.0])
    p3 = np.array([1.0, 0.0, 0.0])
    p = np.array([0.0, 1.0, 0.0])
    print(coordinate_translate(p1, p2, p3, p))

    p1 = np.array([0.3, 0.3, 0.0])
    p2 = np.array([0.3, 1.0, 0.0])
    p3 = np.array([1.0, 0.0, 0.0])
    p = np.array([0.0, 1.0, 0.0])
    print(coordinate_translate(p1, p2, p3, p))
