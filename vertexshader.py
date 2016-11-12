# -*- coding: utf-8 -*-
from shadervarying import ShaderVarying
from shaderuniform import ShaderUniform

class VertexShader(object):
	def __init__(self):
		self.outpos = None

	def run(self):
		raise NotImplementedError


class SimpleVertexShader(VertexShader):
	def __init__(self):
		super(SimpleVertexShader, self).__init__()
		self.inpos = ShaderVarying(0)
		self.mvp = ShaderUniform('mvp')

	def run(self):
		self.outpos = self.mvp.value * self.inpos.value




