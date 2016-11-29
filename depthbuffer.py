# -*- coding: utf-8 -*-
from buffer3d import Buffer3D
import numpy as np

class DepthBuffer(Buffer3D):
	def __init__(self, w, h, initialValue = None):
		super(Buffer3D, self).__init__()
		self.width = w
		self.height = h
		if initialValue:
			self.data = np.full((w, h), initialValue)
		else:
			self.data = np.empty((w, h))

	def put_value(self, x, y, value):
		self.data[x, y] = value

	def get_value(self, x, y, default=None):
		return self.data[x, y] if 0 <= x < self.width and 0 <= y < self.height else default

	def set_all_value(self, value):
		self.data.fill(value)




