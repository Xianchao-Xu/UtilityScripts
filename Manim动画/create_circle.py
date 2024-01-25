# coding: utf-8
# author: xuxc
from manim import (
    Create,
    Circle,
    PINK,
    Scene
)


class CreateCircle(Scene):
    """
    使用方法：manim create_circle.py -v WARNING -ql CreateCircle
    -ql 低质量视频
    -qm 中质量视频
    -qh 高质量视频
    -v WARNING 隐藏不需要的输出信息
    -p 预览
    """
    def construct(self):
        circle = Circle()
        circle.set_fill(PINK, opacity=0.5)
        self.play(Create(circle))
