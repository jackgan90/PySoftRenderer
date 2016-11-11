# -*- coding: utf-8 -*-

class VertexArray(object):
	def __init__(self):
		self.buffers = {}
		self.enabledAttributes = {}
		self.uniqueId = 0
		self.indexBufferId = 0

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
		self.indexBufferId = ib.uniqueId
		return True

	def detachIndexBuffer(self, ibid):
		if ibid not in self.buffers:
			return False
		del self.buffers[ibid]
		self.indexBufferId = 0
		return True

	def enableVertexAttribute(self, attributeIndex, vbid):
		if vbid not in self.buffers:
			return False
		self.enabledAttributes[attributeIndex] = vbid
		return True

	def disableVertexAttribute(self, attributeIndex):
		if attributeIndex in self.enabledAttributes:
			del self.enabledAttributes[attributeIndex]

	def getEnabledVertexBuffer(self, attributeIndex):
		if attributeIndex not in self.enabledAttributes:
			return None
		return self.buffers[self.enabledAttributes[attributeIndex]]

	def getAllEnabledVertexBuffers(self):
		return tuple((attrIdx, self.buffers[vbid]) for attrIdx, vbid in self.enabledAttributes.items())

	def getIndexBuffer(self):
		if self.indexBufferId == 0:
			return None
		return self.buffers[self.indexBufferId]





