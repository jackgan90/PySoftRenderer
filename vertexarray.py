# -*- coding: utf-8 -*-

class VertexArray(object):
	def __init__(self):
		self.buffers = {}
		self.enabledAttributes = {}
		self.uniqueId = 0

	def attachVertexBuffer(self, vb):
		if vb.uniqueId in self.buffers:
			return False
		self.buffers[vb.uniqueId] = vb
		return True

	def detachVertexBuffer(self, vbid):
		if vbid not in self.buffers:
			return False
		del self.buffers[vbid]
		return True

	def attachIndexBuffer(self, ib):
		if ib.uniqueId in self.buffers:
			return False
		self.buffers[ib.uniqueId] = ib
		return True

	def detachIndexBuffer(self, ibid):
		if ibid not in self.buffers:
			return False
		del self.buffers[ibid]
		return True

	def enableVertexAttribute(self, attributeIndex, vbid):
		if vbid not in self.buffers:
			return False
		self.enabledAttributes[attributeIndex] = vbid
		return True

	def disableVertexAttribute(self, attributeIndex):
		if attributeIndex in self.enabledAttributes:
			del self.enabledAttributes[attributeIndex]



