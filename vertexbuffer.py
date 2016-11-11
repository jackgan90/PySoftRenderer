# -*- coding: utf-8 -*-
from srmath import *

class VertexBuffer(object):
	def __init__(self):
		self.buffer = []
		self.uniqueId = 0

	def setBufferData(self, data, stride):
		self.buffer = []
		for i in xrange(0, len(data), stride):
			v = create_vector(stride)
			v.fromList(data[i:i+stride])
			self.buffer.append(v)

	@property
	def bufferSize(self):
		return len(self.buffer)

