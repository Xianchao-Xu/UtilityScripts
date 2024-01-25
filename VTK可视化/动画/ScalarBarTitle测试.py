#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget

from vtkmodules.vtkCommonCore import vtkDoubleArray, vtkLookupTable, vtkPoints, VTK_FONT_FILE
from vtkmodules.vtkCommonDataModel import vtkStructuredGrid
from vtkmodules.vtkInteractionWidgets import (vtkTextRepresentation, vtkTextWidget)
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleTrackballCamera
from vtkmodules.vtkIOImage import vtkPNGWriter
from vtkmodules.vtkRenderingAnnotation import vtkScalarBarActor
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderer,
    vtkTextActor,
    vtkWindowToImageFilter
)

# noinspection PyUnresolvedReferences
import vtkmodules.vtkRenderingOpenGL2
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor as VTKWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.resize(500, 800)

        self.central_widget = QWidget(self)
        self.layout = QVBoxLayout(self.central_widget)
        self.vtk_widget = VTKWidget(self.central_widget)
        self.layout.addWidget(self.vtk_widget)
        self.setCentralWidget(self.central_widget)

        self.n_steps = 4

        nx = 2
        ny = 8
        nz = 1
        points = vtkPoints()
        for j in range(ny):
            for i in range(nx):
                points.InsertNextPoint([i, j * 10, 0])

        grid = vtkStructuredGrid()
        grid.SetDimensions(nx, ny, nz)
        grid.SetPoints(points)

        for step in range(self.n_steps):
            values = vtkDoubleArray()
            property_name = f'step{step}'
            grid_size = nx * ny * nz
            values.SetNumberOfComponents(1)
            values.SetNumberOfTuples(grid_size)
            values.SetName(property_name)
            for j in range(ny):
                for i in range(nx):
                    values.SetValue(j * nx + i, step * i * nx + j)
            grid.GetPointData().AddArray(values)

        lut = vtkLookupTable()
        lut.SetHueRange(0.6667, 0.0)

        self.mapper = vtkDataSetMapper()
        self.mapper.SetInputData(grid)
        self.mapper.SetLookupTable(lut)
        self.mapper.SetScalarModeToUsePointFieldData()

        self.scalar_bar = vtkScalarBarActor()
        self.scalar_bar.SetLookupTable(lut)
        self.scalar_bar.SetPosition(0.1, 0.1)
        self.scalar_bar.SetHeight(0.5)
        self.scalar_bar.SetWidth(0.1)
        self.scalar_bar.SetLabelFormat('%.2f')

        actor = vtkActor()
        actor.SetMapper(self.mapper)
        actor.GetProperty().EdgeVisibilityOn()

        renderer = vtkRenderer()
        renderer.AddActor(actor)
        renderer.AddActor(self.scalar_bar)

        win = self.vtk_widget.GetRenderWindow()
        win.AddRenderer(renderer)

        self.png_writer = vtkPNGWriter()

        iren = win.GetInteractor()
        iren.SetRenderWindow(win)
        style = vtkInteractorStyleTrackballCamera()
        iren.SetInteractorStyle(style)

        self.text = vtkTextActor()
        self.text.GetTextProperty().SetFontFamily(VTK_FONT_FILE)
        self.text.GetTextProperty().SetFontFile(
            r'C:\Users\xuxc\AppData\Local\Microsoft\Windows\Fonts\SourceCodePro-SemiboldIt.ttf')
        self.text.GetTextProperty().SetFontSize(10)
        self.text.GetTextProperty().SetJustificationToLeft()
        text_representation = vtkTextRepresentation()
        text_representation.SetPosition(0.1, 0.62)  # 左下角的位置
        text_representation.SetPosition2(0.25, 0.035)  # 右上角相对左下角的位置
        self.text_widget = vtkTextWidget()
        self.text_widget.SetRepresentation(text_representation)
        self.text_widget.SetTextActor(self.text)
        self.text_widget.SetInteractor(iren)
        self.text_widget.On()
        self.mapper.SelectColorArray('step0')
        self.mapper.SetScalarRange(self.mapper.GetInput().GetPointData().GetArray('step0').GetRange())
        self.text.SetInput("U, Magnitude")
        self.text.SetTextScaleModeToNone()
        self.text.GetTextProperty().SetFontSize(15)

        win.Render()

        self.i_step = 0
        self.timer = QTimer()
        self.timer.start(1000)
        self.timer.timeout.connect(self.change_property_name)

    def change_property_name(self):
        if self.i_step >= self.n_steps:
            self.i_step = 0

        titles = [f"U, X", "U, Y", "U, Z", "U, Magnitude"]
        self.text.SetInput(f"{titles[self.i_step % len(titles)]}")

        property_name = f'step{self.i_step}'
        self.mapper.SelectColorArray(property_name)
        self.mapper.SetScalarRange(self.mapper.GetInput().GetPointData().GetArray(property_name).GetRange())
        win = self.vtk_widget.GetRenderWindow()
        win.Render()

        image_file = f'images/{property_name}.png'
        if not os.path.exists(image_file):
            # w2if如果设置为了类的属性，将不能察觉到图像的变化，每次导出的图像都是第1帧
            # 所以，只能在方法内部，每次创建一个新的对象
            w2if = vtkWindowToImageFilter()
            w2if.SetInput(win)
            w2if.SetInputBufferTypeToRGB()
            w2if.ReadFrontBufferOff()
            w2if.Update()

            self.png_writer.Modified()
            self.png_writer.SetFileName(image_file)
            self.png_writer.SetInputConnection(w2if.GetOutputPort())
            self.png_writer.Write()

        self.i_step += 1


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec_()
