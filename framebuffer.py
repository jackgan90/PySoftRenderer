# -*- coding: utf-8 -*-
from color import Color

class FrameBuffer(object):
	DEFAULT_HEIGHT = 1024
	DEFAULT_WIDTH = 1024
	def __init__(self):
		self.buffer = []
		self._height = self.DEFAULT_HEIGHT
		self._width = self.DEFAULT_WIDTH 

	def reset(self, color = Color.BLACK):
		self.buffer = []
		for x in xrange(self.height):
			for y in xrange(self.width):
				self.buffer.append((int(255 * color.r), int(255 * color.g), int(255 * color.b)))

	@property
	def height(self):
		return self._height

	@property
	def width(self):
		return self._width

	@height.setter
	def height(self, value):
		self._height = value

	@width.setter
	def width(self, value):
		self._width = value
