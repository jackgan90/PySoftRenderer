# -*- coding: utf-8 -*-
from buffer3d import Buffer3D
import numpy as np


class FrameBuffer(Buffer3D):
	def __init__(self, w, h, initialValue):
		super(Buffer3D, self).__init__()
		self.width = w
		self.height = h
		self.data = np.full((w, h), initialValue, dtype=(np.uint8, 3))

	def put_value(self, x, y, value):
		self.data[y, x] = value

	def get_value(self, x, y, default=None):
		return self.data[y, x] if 0 <= x < self.width and 0 <= y < self.height else default

	def set_all_value(self, value):
		self.data = np.full((self.width, self.height), value, dtype=(np.uint8, 3))





