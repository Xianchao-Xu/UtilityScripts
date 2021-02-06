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


def create_spline(points_list, plane='xy'):
    """
    在SpaceClaim的XY、YZ或者ZX平面中中创建样条曲线
    :param points_list: 点集，在XY平面内，形如[[x0, y0], ..., [xn, yn]]
    :param plane: 样条曲线所在平面
    :return: None
    """
    if plane.lower() == 'xy':
        section_plane = Plane.PlaneXY
    elif plane.lower() == 'yz':
        section_plane = Plane.PlaneYZ
    elif plane.lower() == 'zx':
        section_plane = Plane.PlaneZX
    else:
        print('暂不支持在该平面创建样条曲线')
    result = ViewHelper.SetSketchPlane(section_plane)
    points = List[Point2D]()
    for point in points_list:
        x, y = point
        points.Add(Point2D.Create(x, y))
    result = SketchNurbs.CreateFrom2DPoints(False, points)
