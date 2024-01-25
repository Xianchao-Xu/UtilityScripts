#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget

from vtkmodules.vtkCommonCore import vtkDoubleArray, vtkLookupTable, vtkPoints
from vtkmodules.vtkCommonDataModel import vtkStructuredGrid
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleTrackballCamera
from vtkmodules.vtkIOOggTheora import vtkOggTheoraWriter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderer,
    vtkWindowToImageFilter
)
# noinspection PyUnresolvedReferences
import vtkmodules.vtkRenderingOpenGL2
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor as VTKWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.resize(640, 640)

        self.central_widget = QWidget(self)
        self.layout = QVBoxLayout(self.central_widget)
        self.vtk_widget = VTKWidget(self.central_widget)
        self.layout.addWidget(self.vtk_widget)
        self.setCentralWidget(self.central_widget)

        self.ogg_writer = vtkOggTheoraWriter()
        self.ogg_writer.SetFileName('videos/video.avi')

        self.grid = vtkStructuredGrid()
        self.mapper = vtkDataSetMapper()

        self.plate_length = 0
        self.plate_width = 0
        self.slices_x = 0
        self.slices_y = 0
        self.t = 5
        self.dt = 0.1
        self.up_bound = 0
        self.current_t = 0

        self.record = True

        self.timer = QTimer()

        self.timer.timeout.connect(self.change_property_name)

    def add_plate(self, length: float, width: float, slices_x: int, slices_y: int):
        self.plate_length = length
        self.plate_width = width
        self.slices_x = slices_x
        self.slices_y = slices_y

        x_size = length / slices_x
        y_size = width / slices_y

        points = vtkPoints()
        for j in range(slices_y + 1):
            for i in range(slices_x + 1):
                x = x_size * i
                y = y_size * j
                z = 0
                points.InsertNextPoint([x, y, z])

        self.grid.SetDimensions(slices_x + 1, slices_y + 1, 1)
        self.grid.SetPoints(points)

        current_t = 0
        while current_t < self.t:
            values = vtkDoubleArray()
            property_name = f'time{current_t:.2f}'
            grid_size = (slices_x + 1) * (slices_y + 1)
            values.SetNumberOfComponents(1)
            values.SetNumberOfTuples(grid_size)
            values.SetName(property_name)
            for i in range(grid_size):
                values.SetValue(i, i * current_t)
                self.up_bound = i * current_t

            self.grid.GetPointData().AddArray(values)
            current_t += self.dt

        lut = vtkLookupTable()
        lut.SetHueRange(0.6667, 0.0)

        self.mapper.SetInputData(self.grid)
        self.mapper.SetLookupTable(lut)
        self.mapper.SetScalarModeToUsePointFieldData()
        self.mapper.SelectColorArray('time0.00')

        actor = vtkActor()
        actor.SetMapper(self.mapper)
        actor.GetProperty().EdgeVisibilityOn()

        render = vtkRenderer()
        render.AddActor(actor)

        win = self.vtk_widget.GetRenderWindow()
        win.AddRenderer(render)

        iren = win.GetInteractor()
        style = vtkInteractorStyleTrackballCamera()
        iren.SetInteractorStyle(style)

        win.Render()

        w2if = vtkWindowToImageFilter()
        w2if.SetInput(win)
        w2if.SetInputBufferTypeToRGB()
        w2if.ReadFrontBufferOff()
        w2if.Update()
        self.ogg_writer.SetInputData(w2if.GetOutput())
        self.ogg_writer.SetQuality(2)
        self.ogg_writer.SetRate(24)
        self.ogg_writer.Start()
        # self.ogg_writer.Write()

        self.timer.start(100)

    def change_property_name(self):
        self.current_t += self.dt
        if self.current_t > self.t:
            self.current_t = 0
            self.ogg_writer.End()
            self.record = False

        property_name = f'time{self.current_t:.2f}'
        self.mapper.SelectColorArray(property_name)
        self.mapper.SetScalarRange([0, self.up_bound])
        self.vtk_widget.GetRenderWindow().Render()

        if self.record:
            w2if = vtkWindowToImageFilter()
            w2if.SetInput(self.vtk_widget.GetRenderWindow())
            w2if.SetInputBufferTypeToRGB()
            w2if.ReadFrontBufferOff()
            w2if.Update()

            self.ogg_writer.SetInputData(w2if.GetOutput())
            self.ogg_writer.Write()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.add_plate(10., 5., 10, 5)
    window.show()
    app.exec_()
