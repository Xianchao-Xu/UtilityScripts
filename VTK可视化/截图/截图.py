# coding: utf-8
# author: xuxc

from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkIOImage import vtkPNGWriter
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleTrackballCamera
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkWindowToImageFilter
)
# noinspection PyUnresolvedReferences
import vtkmodules.vtkRenderingOpenGL2

source = vtkSphereSource()
source.SetCenter(0, 0, 0)
source.SetRadius(5.0)

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(source.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(1, 0, 0)  # (R,G,B)

ren = vtkRenderer()
ren.AddActor(actor)

renWin = vtkRenderWindow()
renWin.AddRenderer(ren)
renWin.Render()

w2if = vtkWindowToImageFilter()
w2if.SetInput(renWin)
w2if.Update()

writer = vtkPNGWriter()
writer.SetFileName("screenshot.png")
writer.SetInputConnection(w2if.GetOutputPort())
writer.Write()

iren = vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
style = vtkInteractorStyleTrackballCamera()
iren.SetInteractorStyle(style)

iren.Initialize()
iren.Start()
