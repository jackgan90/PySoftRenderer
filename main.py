# -*- coding: utf-8 -*-
import window
import pipeline
if __name__ == '__main__':
	pipeline.get_pipeline().init()
	w = window.Window(pipeline.get_pipeline())
	w.init()

