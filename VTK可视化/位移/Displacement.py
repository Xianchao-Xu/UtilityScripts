#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget

from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor as VTKWidget
from vtkmodules.vtkCommonCore import vtkDoubleArray, vtkPoints
from vtkmodules.vtkCommonDataModel import VTK_HEXAHEDRON, vtkUnstructuredGrid
from vtkmodules.vtkFiltersGeneral import vtkWarpVector
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleTrackballCamera
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderer
)

# noinspection PyUnresolvedReferences
import vtkmodules.vtkRenderingOpenGL2


pts = [
    [0, 0, 0], [1, 0, 0], [2, 0, 0],
    [0, 1, 0], [1, 1, 0], [2, 1, 0],
    [0, 2, 0], [1, 2, 0], [2, 2, 0],
    [0, 0, 1], [1, 0, 1], [2, 0, 1],
    [0, 1, 1], [1, 1, 1], [2, 1, 1],
    [0, 2, 1], [1, 2, 1], [2, 2, 1],
    [0, 0, 2], [1, 0, 2], [2, 0, 2],
    [0, 1, 2], [1, 1, 2], [2, 1, 2],
    [0, 2, 2], [1, 2, 2], [2, 2, 2],
]

elements = [
    [0, 1, 4, 3, 9, 10, 13, 12],
    [1, 2, 5, 4, 10, 11, 14, 13],
    [3, 4, 7, 6, 12, 13, 16, 15],
    [4, 5, 8, 7, 13, 14, 17, 16],
    [9, 10, 13, 12, 18, 19, 22, 21],
    [10, 11, 14, 13, 19, 20, 23, 22],
    [12, 13, 16, 15, 21, 22, 25, 24],
    [13, 14, 17, 16, 22, 23, 26, 25]
]

fields = {
    'x': [
        [0, 0, 0], [0, 0, 0], [0, 0, 0],
        [0, 0, 0], [0, 0, 0], [0, 0, 0],
        [0, 0, 0], [0, 0, 0], [0, 0, 0],
        [0.1, 0, 0], [0.1, 0, 0], [0.1, 0, 0],
        [0.1, 0, 0], [0.1, 0, 0], [0.1, 0, 0],
        [0.1, 0, 0], [0.1, 0, 0], [0.1, 0, 0],
        [0.2, 0, 0], [0.2, 0, 0], [0.2, 0, 0],
        [0.2, 0, 0], [0.2, 0, 0], [0.2, 0, 0],
        [0.2, 0, 0], [0.2, 0, 0], [0.2, 0, 0]
    ],
    'y': [
        [0, 0, 0], [0, 0, 0], [0, 0, 0],
        [0, 0, 0], [0, 0, 0], [0, 0, 0],
        [0, 0, 0], [0, 0, 0], [0, 0, 0],
        [0, 0.1, 0], [0, 0.1, 0], [0, 0.1, 0],
        [0, 0.1, 0], [0, 0.1, 0], [0, 0.1, 0],
        [0, 0.1, 0], [0, 0.1, 0], [0, 0.1, 0],
        [0, 0.2, 0], [0, 0.2, 0], [0, 0.2, 0],
        [0, 0.2, 0], [0, 0.2, 0], [0, 0.2, 0],
        [0, 0.2, 0], [0, 0.2, 0], [0, 0.2, 0]
    ],
    'z': [
        [0, 0, 0], [0, 0, 0], [0, 0, 0],
        [0, 0, 0], [0, 0, 0], [0, 0, 0],
        [0, 0, 0], [0, 0, 0], [0, 0, 0],
        [0, 0, 0.1], [0, 0, 0.1], [0, 0, 0.1],
        [0, 0, 0.1], [0, 0, 0.1], [0, 0, 0.1],
        [0, 0, 0.1], [0, 0, 0.1], [0, 0, 0.1],
        [0, 0, 0.2], [0, 0, 0.2], [0, 0, 0.2],
        [0, 0, 0.2], [0, 0, 0.2], [0, 0, 0.2],
        [0, 0, 0.2], [0, 0, 0.2], [0, 0, 0.2]
    ]
}


class MainWindow(QMainWindow):
    def __init__(self, w: int, h: int):
        super(MainWindow, self).__init__()
        self.resize(w, h)

        self.central_widget = QWidget(self)
        self.layout = QVBoxLayout(self.central_widget)
        self.vtk_widget = VTKWidget(self.central_widget)
        self.layout.addWidget(self.vtk_widget)
        self.setCentralWidget(self.central_widget)

        self.win = self.vtk_widget.GetRenderWindow()
        iren = self.win.GetInteractor()
        style = vtkInteractorStyleTrackballCamera()
        iren.SetInteractorStyle(style)

        self.ugrid = vtkUnstructuredGrid()
        for cell in elements:
            self.ugrid.InsertNextCell(VTK_HEXAHEDRON, 8, cell)
        points = vtkPoints()
        for i in range(len(pts)):
            points.InsertPoint(i, pts[i])
        self.ugrid.SetPoints(points)

        for field_name in fields:
            displacement = vtkDoubleArray()
            displacement.SetName(field_name)
            values = fields[field_name]
            displacement.SetNumberOfComponents(len(values[0]))
            displacement.SetNumberOfTuples(len(values))
            for i in range(len(values)):
                value = values[i]
                displacement.SetTuple3(i, value[0], value[1], value[2])
            self.ugrid.GetPointData().AddArray(displacement)

        mapper = vtkDataSetMapper()
        mapper.SetInputData(self.ugrid)

        self.origin_actor = vtkActor()
        self.origin_actor.SetMapper(mapper)
        self.origin_actor.GetProperty().EdgeVisibilityOn()
        self.origin_actor.GetProperty().SetOpacity(0.2)

        renderer = vtkRenderer()
        renderer.AddActor(self.origin_actor)
        self.deformation_actor = vtkActor()
        renderer.AddActor(self.deformation_actor)

        self.win.AddRenderer(renderer)

        self.win.Render()

        self.i_step = 0
        self.timer = QTimer()
        self.timer.start(1000)
        self.timer.timeout.connect(self.change_field_name)

    def change_field_name(self):
        field_names = list(fields.keys())
        if self.i_step >= len(field_names):
            self.i_step = 0

        warp = vtkWarpVector()
        self.ugrid.GetPointData().SetActiveVectors(field_names[self.i_step])
        warp.SetInputData(self.ugrid)
        warp.SetScaleFactor(2)
        warp_mapper = vtkDataSetMapper()
        warp_mapper.SetInputConnection(warp.GetOutputPort())
        self.deformation_actor.SetMapper(warp_mapper)
        self.deformation_actor.GetProperty().SetColor(0.5, 0, 0)
        self.win.Render()

        self.i_step += 1


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow(960, 800)
    w.show()
    app.exec_()
