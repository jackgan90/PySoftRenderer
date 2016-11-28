# -*- coding: utf-8 -*-
import config
import tkinterwindow
import pygamewindow
import openglwindow
import pipeline
if __name__ == '__main__':
	pipeline.get_pipeline().init()
	if config.WINDOW_SYSTEM == 'pygame':
		w = pygamewindow.PyGameWindow(pipeline.get_pipeline())
	elif config.WINDOW_SYSTEM == 'tkinter':
		w = tkinterwindow.TkinterWindow(pipeline.get_pipeline())
	elif config.WINDOW_SYSTEM == 'opengl':
		w = openglwindow.OpenGLWindow(pipeline.get_pipeline())

	w.init()

