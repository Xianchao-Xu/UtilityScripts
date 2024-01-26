# coding: utf-8
# author: xuxc

from math import sqrt
from random import random

import numpy as np


def cross(vec1: np.ndarray, vec2: np.ndarray) -> np.ndarray:
    return np.cross(vec1, vec2)


def trans_matrix(pnt1: np.array, pnt2: np.array, pnt3: np.array):
    t33 = np.zeros((3, 3))
    v12 = pnt2 - pnt1
    v13 = pnt3 - pnt1
    x21, y21, z21 = v12
    x31, y31, z31 = v13
    length = sqrt(x21 * x21 + y21 * y21 + z21 * z21)
    a123 = sqrt((y21 * z31 - y31 * z21)**2 + (z21 * x31 - z31 * x21)**2 + (x21 * y31 - x31 * y21)**2)
    t33[0, 0] = x21 / length  # lx
    t33[0, 1] = y21 / length  # mx
    t33[0, 2] = z21 / length  # nx
    t33[2, 0] = (y21 * z31 - y31 * z21) / a123  # lz
    t33[2, 1] = (z21 * x31 - z31 * x21) / a123  # mz
    t33[2, 2] = (x21 * y31 - x31 * y21) / a123  # nz
    t33[1, 0] = t33[2, 1] * t33[0, 2] - t33[2, 2] * t33[0, 1]
    t33[1, 1] = t33[2, 2] * t33[0, 0] - t33[2, 0] * t33[0, 2]
    t33[1, 2] = t33[2, 0] * t33[0, 1] - t33[2, 1] * t33[0, 0]
    return t33


def trans_matrix2(pnt1: np.array, pnt2: np.array, pnt3: np.array):
    t33 = np.zeros((3, 3))
    v12 = pnt2 - pnt1
    v13 = pnt3 - pnt1
    x21, y21, z21 = v12
    len12 = sqrt(x21 * x21 + y21 * y21 + z21 * z21)
    x_local = v12 / len12
    z_local = cross(x_local, v13)
    z_local /= np.linalg.norm(z_local)
    y_local = cross(z_local, x_local)
    x_global = np.array([1., 0., 0.])
    y_global = np.array([0., 1., 0.])
    z_global = np.array([0., 0., 1.])
    t33[0, 0] = x_local.dot(x_global)
    t33[0, 1] = x_local.dot(y_global)
    t33[0, 2] = x_local.dot(z_global)
    t33[1, 0] = y_local.dot(x_global)
    t33[1, 1] = y_local.dot(y_global)
    t33[1, 2] = y_local.dot(z_global)
    t33[2, 0] = z_local.dot(x_global)
    t33[2, 1] = z_local.dot(y_global)
    t33[2, 2] = z_local.dot(z_global)
    return t33


if __name__ == '__main__':
    p1 = np.array([random() for _ in range(3)])
    p2 = np.array([random() for _ in range(3)])
    p3 = np.array([random() for _ in range(3)])
    t1 = trans_matrix(p1, p2, p3)
    t2 = trans_matrix2(p1, p2, p3)
    print(t1 - t2)
