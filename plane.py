# -*- coding: utf-8 -*-

class Plane(object):
	def __init__(self, width = 1, height = 1):
		self.vertices = (
			-width / 2.0, 0.0, height / 2.0,
			width / 2.0, 0.0, height / 2.0,
			-width / 2.0, 0.0, -height / 2.0,
			width / 2.0, 0.0, -height / 2.0,
		)
		self.colors = (
			1.0, 0.0, 0.0,
			1.0, 0.0, 0.0,
			1.0, 1.0, 0.0,
			1.0, 0.0, 0.0,
		)
		self.uvs = (
			0.0, 0.0, 1.0,
			0.0, 1.0, 1.0,
			1.0, 0.0, 1.0,
			1.0, 1.0, 1.0,
		)
		self.indices = (
			0, 1, 2,
			2, 1, 3,
		)



