# -*- coding: utf-8 -*-
import tkinterwindow
import pygamewindow
import pipeline
if __name__ == '__main__':
	pipeline.get_pipeline().init()
	# w = tkinterwindow.TkinterWindow(pipeline.get_pipeline())
	w = pygamewindow.PyGameWindow(pipeline.get_pipeline())
	w.init()

