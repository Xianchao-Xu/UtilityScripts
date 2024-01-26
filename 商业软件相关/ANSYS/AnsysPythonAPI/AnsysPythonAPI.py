# coding: utf-8
# author: xuxc
def export_deformation():
    """
    通过ANSYS的Python接口导出节点位移数据
    :return:
    """
    analysis = ExtAPI.DataModel.Project.Model.Analyses[0]
    output_file = analysis.WorkingDir + 'deformation.dat'
    mesh_obj = analysis.MeshData
    node_ids = mesh_obj.NodeIds
    node_ids.Sort()
    reader = analysis.GetResultsData()
    disp = reader.GetResult('U')
    with open(output_file, 'w') as fw:
        for node_id in node_ids:
            node = mesh_obj.NodeById(node_id)
            x = node.X
            y = node.Y
            z = node.Z
            dx, dy, dz = disp.GetNodeValues(node_id)
            fw.write('{:20.8e} {:20.8e} {:20.8e} {:20.8e} {:20.8e} {:20.8e}\n'.format(
                x, y, z, dx, dy, dz
            ))


def export_to_vtk():
    analysis = ExtAPI.DataModel.Project.Model.Analyses[0]
    mesh_obj = analysis.MeshData
    element_ids = mesh_obj.ElementIds
    node_ids = mesh_obj.NodeIds
    node_ids.Sort()
    vtk_file = analysis.WorkingDir + 'deformation.vtk'
    fw = open(vtk_file, 'w')
    fw.write('# vtk DataFile Version 2.0\n')
    fw.write('ANSYS Mechanical to vtk unstructured grid\n')
    fw.write('ASCII\n\n')

    fw.write('DATASET UNSTRUCTURED_GRID\n')
    fw.write('POINTS {} float\n'.format(len(node_ids)))
    for node_id in node_ids:
        node = mesh_obj.NodeById(node_id)
        x = node.X
        y = node.Y
        z = node.Z
        fw.write('{:20.8e} {:20.8e} {:20.8e}\n'.format(x, y, z))

    polygon_list = []
    for element_id in element_ids:
        element = mesh_obj.ElementById(element_id)
        element_node_ids = element.NodeIds
        polygon_list.append(len(element_node_ids))
        for node_id in element_node_ids:
            polygon_list.append(node_ids.IndexOf(node_id))
        polygon_list.append(-1)
    fw.write('\nCELLS {} {}\n'.format(len(element_ids), len(polygon_list)-len(element_ids)))
    for point_id in polygon_list:
        if point_id == -1:
            point_id = '\n'
        fw.write(' {}'.format(point_id))

    fw.write('CELL_TYPES {}\n'.format(len(element_ids)))
    for element_id in element_ids:
        element = mesh_obj.ElementById(element_id)
        if len(element.NodeIds) == 4:
            fw.write(' 10\n')
        elif len(element.NodeIds) == 8:
            fw.write(' 12\n')
        elif len(element.NodeIds) == 10:
            fw.write(' 24\n')
        elif len(element.NodeIds) == 20:
            fw.write(' 25\n')

    fw.write('\nPOINT_DATA {}\n'.format(len(node_ids)))
    reader = analysis.GetResultsData()
    disp = reader.GetResult('U')
    list_time_freq = reader.ListTimeFreq
    for time_freq in list_time_freq:
        fw.write('VECTORS Displacement_Time_{} float\n'.format(time_freq))
        reader.CurrentTimeFreq = time_freq
        for node_id in node_ids:
            dx, dy, dz = disp.GetNodeValues(node_id)
            fw.write('{:20.8e} {:20.8e} {:20.8e}\n'.format(dx, dy, dz))

    fw.close()
