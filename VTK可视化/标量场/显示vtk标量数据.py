# coding: utf-8
# author: xuxc

from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleTrackballCamera
from vtkmodules.vtkIOLegacy import vtkUnstructuredGridReader
from vtkmodules.vtkRenderingAnnotation import vtkScalarBarActor
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor
)
# noinspection PyUnresolvedReferences
import vtkmodules.vtkRenderingOpenGL2

scalar_name = 'y'
reader = vtkUnstructuredGridReader()
reader.SetFileName('test.vtk')
reader.SetScalarsName(scalar_name)
reader.Update()

lut = vtkLookupTable()
lut.SetHueRange(0.6667, 0.0)

data_mapper = vtkDataSetMapper()
data_mapper.SetLookupTable(lut)
data_mapper.SetInputConnection(reader.GetOutputPort())
data_mapper.SetScalarRange(reader.GetOutput().GetScalarRange())

data_actor = vtkActor()
data_actor.SetMapper(data_mapper)
data_actor.GetProperty().SetLineWidth(3)

scalar_bar = vtkScalarBarActor()
scalar_bar.SetLookupTable(data_mapper.GetLookupTable())
scalar_bar.SetTitle('Displacement: {}\n'.format(scalar_name))
scalar_bar.GetTitleTextProperty().SetColor(0, 0, 0)
scalar_bar.SetNumberOfLabels(10)
scalar_bar.GetLabelTextProperty().SetFontFamilyToCourier()
scalar_bar.GetLabelTextProperty().BoldOff()
scalar_bar.GetLabelTextProperty().ShadowOff()
scalar_bar.GetProperty().SetColor(0, 0, 0)

ren = vtkRenderer()
ren.SetBackground(1, 1, 1)
ren.AddActor(data_actor)
ren.AddActor(scalar_bar)
ren.ResetCamera()

ren_win = vtkRenderWindow()
ren_win.AddRenderer(ren)
ren_win.SetSize(720, 360)
ren_win.Render()

iren = vtkRenderWindowInteractor()
style = vtkInteractorStyleTrackballCamera()
iren.SetRenderWindow(ren_win)
iren.SetInteractorStyle(style)

iren.Initialize()
iren.Start()
