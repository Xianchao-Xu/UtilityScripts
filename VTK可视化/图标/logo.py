# coding: utf-8
# author: xuxc
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleTrackballCamera
from vtkmodules.vtkInteractionWidgets import vtkLogoRepresentation, vtkLogoWidget
from vtkmodules.vtkIOImage import vtkPNGReader
from vtkmodules.vtkRenderingCore import (
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor
)
# noinspection PyUnresolvedReferences
import vtkmodules.vtkRenderingOpenGL2

png_reader = vtkPNGReader()
png_reader.SetFileName('vtk_logo-main1.png')
png_reader.Update()

logo_representation = vtkLogoRepresentation()
logo_representation.SetImage(png_reader.GetOutput())
logo_representation.SetPosition(0.85, 0.05)
logo_representation.SetPosition2(0.15, 0.15)
logo_representation.GetImageProperty().SetOpacity(1.0)

ren = vtkRenderer()
ren.SetBackground(1, 1, 1)

ren_win = vtkRenderWindow()
ren_win.AddRenderer(ren)
ren_win.SetSize(480, 480)

iren = vtkRenderWindowInteractor()
style = vtkInteractorStyleTrackballCamera()
iren.SetRenderWindow(ren_win)
iren.SetInteractorStyle(style)

logo_widget = vtkLogoWidget()
logo_widget.SetRepresentation(logo_representation)
logo_widget.SetInteractor(iren)
logo_widget.On()
logo_widget.ProcessEventsOff()

iren.Initialize()
iren.Start()
