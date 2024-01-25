# coding: utf-8
# author: xuxc

from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor
)
# noinspection PyUnresolvedReferences
import vtkmodules.vtkRenderingOpenGL2
# noinspection PyUnresolvedReferences
import vtkmodules.vtkInteractionStyle


class TimerCallback(object):
    def __init__(self):
        self.timer_count = 0

    def execute(self, obj, event):
        self.actor.SetPosition(self.timer_count % 16 - 8,
                               self.timer_count % 16 - 8, 0)
        iren = obj
        iren.GetRenderWindow().Render()
        self.timer_count += 1


def main():
    sphere_source = vtkSphereSource()
    sphere_source.SetCenter(0.0, 0.0, 0.0)
    sphere_source.SetRadius(3)

    mapper = vtkPolyDataMapper()
    mapper.SetInputConnection(sphere_source.GetOutputPort())

    actor = vtkActor()
    actor.SetMapper(mapper)

    renderer = vtkRenderer()
    renderer.AddActor(actor)
    renderer.SetBackground(1, 1, 1)

    window = vtkRenderWindow()
    window.SetWindowName("Test")
    window.SetSize(320, 320)
    window.AddRenderer(renderer)

    interactor = vtkRenderWindowInteractor()
    interactor.SetRenderWindow(window)

    interactor.Initialize()

    cb = TimerCallback()
    cb.actor = actor
    interactor.AddObserver('TimerEvent', cb.execute)
    interactor.CreateRepeatingTimer(100)

    interactor.Start()


if __name__ == '__main__':
    main()
