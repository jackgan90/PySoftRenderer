# -*- coding: utf-8 -*-
import helpers
from vertexarray import VertexArray
from vertexbuffer import VertexBuffer
from indexbuffer import IndexBuffer

class Pipeline(object):
	def __init__(self):
		pass

	def createVertexArray(self):
		va = VertexArray()
		va.uniqueId = helpers.genid()
		return va

	def createVertexBuffer(self):
		vb = VertexBuffer()
		vb.uniqueId = helpers.genid()
		return vb

	def createIndexBuffer(self):
		ib = IndexBuffer()
		ib.uniqueId = helpers.genid()
		return ib

	def drawVertexArray(self, va):
		pass




