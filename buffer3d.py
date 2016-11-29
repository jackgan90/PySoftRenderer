# -*- coding: utf-8 -*-
import resource

class Buffer3D(resource.Resource):
	def __init__(self, w, h, initialValue = None):
		super(Buffer3D, self).__init__()
		self.width = w
		self.height = h
		self.data = [initialValue] * (self.width * self.height)

	def put_value(self, x, y, value):
		if 0 <= x < self.width and 0 <= y < self.height:
			self.data[y * self.width + x] = value

	def get_value(self, x, y, default=None):
		return self.data[y * self.width + x] if 0 <= x < self.width and 0 <= y < self.height else default

	def set_all_value(self, value):
		self.data = [value] * (self.width * self.height)




