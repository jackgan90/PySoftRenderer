# -*- coding: utf-8 -*-
from window import Window
from framebuffer import FrameBuffer
from color import Color
fb = FrameBuffer()
fb.reset()
window = Window()
window.show(fb)

