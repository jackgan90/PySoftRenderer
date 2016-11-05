# -*- coding: utf-8 -*-

class Color(object):
	def __init__(self, r=0.0, g=0.0, b=0.0, a=0.0):
		self.r = r
		self.g = g
		self.b = b
		self.a = a



Color.WHITE = Color(1.0, 1.0, 1.0, 1.0)
Color.BLACK = Color(0.0, 0.0, 0.0, 0.0)
Color.RED = Color(1.0, 0.0, 0.0, 1.0)
Color.GREEN = Color(0.0, 1.0, 0.0, 1.0)
Color.BLUE = Color(0.0, 0.0, 1.0, 1.0)
Color.YELLOW = Color(1.0, 1.0, 0.0, 1.0)

