# -*- coding: utf-8 -*-
import resource

class Buffer3D(resource.Resource):
	def __init__(self, w, h, initialValue = None):
		super(Buffer3D, self).__init__()
		self.width = w
		self.height = h
		if not initialValue:
			self.data = []
		else:
			self.data = [initialValue] * (self.width * self.height)

	def put_value(self, x, y, value):
		if 0 <= x < self.width and 0 <= y < self.height:
			self.data[y * self.width + x] = value

	def get_value(self, x, y, default=None):
		if 0 <= x < self.width and 0 <= y < self.height:
			return self.data[y * self.width + x]
		else:
			return default

	def set_all_value(self, value):
		self.data = [value] * (self.width * self.height)




