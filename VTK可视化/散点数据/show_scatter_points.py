# coding: utf-8
# author: xuxc
# noinspection PyUnresolvedReferences
import vtkmodules.vtkInteractionStyle
# noinspection PyUnresolvedReferences
import vtkmodules.vtkRenderingOpenGL2
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkIOLegacy import vtkSimplePointsReader
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleTrackballCamera
from vtkmodules.vtkRenderingCore import (
    vtkPolyDataMapper,
    vtkActor,
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor
)
import numpy as np

with open('points.xyz', 'w') as fw:
    for x in np.linspace(0, 121.4, 11):
        for y in np.linspace(0, 26.4, 11):
            for z in np.linspace(0, 31, 11):
                fw.write('{:10.4f} {:10.4f} {:10.4f}\n'.format(x, y, z))

colors = vtkNamedColors()

reader = vtkSimplePointsReader()
reader.SetFileName('points.xyz')
reader.Update()

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(reader.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetPointSize(6)
actor.GetProperty().SetColor(colors.GetColor3d('Gold'))

renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.GradientBackgroundOn()
renderer.SetBackground(.1, .1, .1)
renderer.SetBackground2(0.2, 0.2, 0.2)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(960, 960)

style = vtkInteractorStyleTrackballCamera()

interactor = vtkRenderWindowInteractor()
interactor.SetInteractorStyle(style)
interactor.SetRenderWindow(render_window)

render_window.Render()
interactor.Start()
