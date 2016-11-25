# -*- coding: utf-8 -*-
import math

class Cube(object):
	def __init__(self, size = 1):
		self.vertices = (
			-0.5 * size, -0.5 * size, 0.5 * size,	#front bottom left
			0.5 * size, -0.5 * size, 0.5 * size,	#front bottom right
			0.5 * size, 0.5 * size, 0.5 * size,		#front top right
			-0.5 * size, 0.5 * size, 0.5 * size,	#front top left
			-0.5 * size, -0.5 * size, -0.5 * size,	#back bottom left
			0.5 * size, -0.5 * size, -0.5 * size,	#back bottom right
			0.5 * size, 0.5 * size, -0.5 * size,	#back top right
			-0.5 * size, 0.5 * size, -0.5 * size,	#back top left
		)
		self.colors = (
			1.0, 1.0, 1.0,
			1.0, 0.0, 0.0,
			0.0, 1.0, 0.0,
			0.0, 0.0, 1.0,
			1.0, 1.0, 0.0,
			0.0, 1.0, 1.0,
			1.0, 0.0, 1.0,
			0.0, 0.0, 0.0,
			0.1, 0.7, 0.8,
		)
		sqrt3Over3 = math.sqrt(3.0) / 3.0
		self.normals = (
			-sqrt3Over3, -sqrt3Over3, sqrt3Over3,
			sqrt3Over3, -sqrt3Over3, sqrt3Over3,
			sqrt3Over3, sqrt3Over3, sqrt3Over3,
			-sqrt3Over3, sqrt3Over3, sqrt3Over3,
			-sqrt3Over3, -sqrt3Over3, -sqrt3Over3,
			sqrt3Over3, -sqrt3Over3, -sqrt3Over3,
			sqrt3Over3, sqrt3Over3, -sqrt3Over3,
			-sqrt3Over3, sqrt3Over3, -sqrt3Over3,
		)
		self.indices = (
			0, 1, 3,
			3, 1, 2,
			2, 1, 5,
			2, 5, 6,
			7, 6, 5,
			7, 5, 4,
			3, 7, 4,
			3, 4, 0,
			3, 2, 7,
			7, 2, 6,
			4, 0, 1,
			4, 1, 5,
		)
