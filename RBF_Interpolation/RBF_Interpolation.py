# coding: utf-8
# author: xuxc
from math import sqrt

from scipy.linalg import solve
import numpy as np


def rbf_coefficient(support_points, support_values, radius, function_name='C2'):
    """
    计算并返回径向基(radical basis function, RBF)插值函数的插值系数
    :param support_points: 径向基插值的支撑点
    :param support_values: 支撑点上的物理量，如位移、压力等
    :param radius: 径向基函数的作用半径
    :param function_name: 使用的径向基函数，默认为 Wendland C2 函数
    :return: coefficient_mat, 径向基函数的插值系数矩阵
    """
    # 支撑点的数量、问题的维数
    num_support_points, dim = np.shape(support_points)
    coefficient_mat = np.zeros((num_support_points, dim), dtype=np.float)
    phi_mat = np.zeros((num_support_points, num_support_points), dtype=np.float)
    for i in range(num_support_points):
        for j in range(num_support_points):
            eta = 0
            for k in range(dim):
                eta += (support_points[i, k] - support_points[j, k]) ** 2
            eta = sqrt(eta) / radius
            if eta <= 1:
                if function_name == 'C2':
                    phi_mat[i, j] = (1 - eta) ** 4 * (4 * eta + 1)
    for i in range(dim):
        coefficient_mat[:, i] = solve(phi_mat, support_values[:, i])

    return coefficient_mat


def rbf_interpolation(support_points, coefficient_mat, radius, interpolation_points, function_name='C2'):
    """
    计算并返回RBF插值的结果
    :param support_points: 支撑点
    :param coefficient_mat: 插值系数矩阵
    :param radius: 插值函数作用半径
    :param interpolation_points: 插值点
    :param function_name: 插值函数名，默认为 Wendland C2
    :return: interpolation_values, 插值点的物理量
    """
    num_interpolation_points, dim = np.shape(interpolation_points)
    num_support_points = np.shape(support_points)[0]
    interpolation_values = np.zeros((num_interpolation_points, dim), dtype=np.float)
    for i in range(num_interpolation_points):
        for j in range(num_support_points):
            eta = 0
            for k in range(dim):
                eta += (interpolation_points[i, k] - support_points[j, k]) ** 2
            eta = sqrt(eta) / radius
            if eta > 1:
                phi = 0
            else:
                if function_name == 'C2':
                    phi = (1 - eta) ** 4 * (4 * eta + 1)
                else:
                    print('暂不支持此插值函数')
                    return

            for k in range(dim):
                interpolation_values[i, k] += coefficient_mat[j, k] * phi
    return interpolation_values


def test():
    boundary_points = np.loadtxt('test_files/ansys_125elements.dat', usecols=(0, 1, 2))
    boundary_displacement = np.loadtxt('test_files/ansys_125elements.dat', usecols=(3, 4, 5))
    r = 1
    coefficient = rbf_coefficient(boundary_points, boundary_displacement, r)

    input_file = 'test_files/ansys_1000elements.dat'
    output_file = 'test_files/rbf_1000elements.dat'
    interpolation_points = np.loadtxt(input_file, usecols=(0, 1, 2))
    values = rbf_interpolation(boundary_points, coefficient, r, interpolation_points)
    num_interpolation_points, dim = np.shape(values)
    with open(output_file, 'w') as fw:
        for i in range(num_interpolation_points):
            for j in range(dim):
                fw.write('{:20.8e} '.format(interpolation_points[i, j]))
            for j in range(dim):
                fw.write('{:20.8e} '.format(values[i, j]))
            fw.write('\n')

    input_file = 'test_files/ansys_tetra10.dat'
    output_file = 'test_files/rbf_tetra10.dat'
    interpolation_points = np.loadtxt(input_file, usecols=(0, 1, 2))
    values = rbf_interpolation(boundary_points, coefficient, r, interpolation_points)
    num_interpolation_points, dim = np.shape(values)
    with open(output_file, 'w') as fw:
        for i in range(num_interpolation_points):
            for j in range(dim):
                fw.write('{:20.8e} '.format(interpolation_points[i, j]))
            for j in range(dim):
                fw.write('{:20.8e} '.format(values[i, j]))
            fw.write('\n')

    input_file = 'test_files/ansys_4000elements_2nd_order.dat'
    output_file = 'test_files/rbf_4000elements_2nd_order.dat'
    interpolation_points = np.loadtxt(input_file, usecols=(0, 1, 2))
    values = rbf_interpolation(boundary_points, coefficient, r, interpolation_points)
    num_interpolation_points, dim = np.shape(values)
    with open(output_file, 'w') as fw:
        for i in range(num_interpolation_points):
            for j in range(dim):
                fw.write('{:20.8e} '.format(interpolation_points[i, j]))
            for j in range(dim):
                fw.write('{:20.8e} '.format(values[i, j]))
            fw.write('\n')


if __name__ == '__main__':
    test()
