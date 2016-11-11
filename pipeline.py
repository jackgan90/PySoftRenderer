# -*- coding: utf-8 -*-
import helpers
from vertexarray import VertexArray
from vertexbuffer import VertexBuffer
from indexbuffer import IndexBuffer
from vertexshader import SimpleVertexShader
from fragmentshader import SimpleFragmentShader

class Pipeline(object):
	def __init__(self):
		self.currentVS = None
		self.currentFS = None

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

	def createVertexShader(self, shaderName = ''):
		return self.createShader(shaderName, SimpleVertexShader)

	def createFragmentShader(self, shaderName = ''):
		return self.createShader(shaderName, SimpleFragmentShader)

	def useVertexShader(self, vs):
		self.currentVS = vs

	def useFragmentShader(self, fs):
		self.currentFS = fs

	def createShader(self, shaderName, fallback):
		try:
			module = __import__(shaderName, fromlist=[''])
			shaderClass = getattr(module, shaderName, None)
			if shaderClass:
				return shaderClass()
			else:
				return fallback()
		except:
			return fallback()


	def drawVertexArray(self, va):
		if not self.currentVS:
			return

		if not self.currentFS:
			return

		vbs = va.getAllEnabledVertexBuffers()
		if not vbs:
			return



		





