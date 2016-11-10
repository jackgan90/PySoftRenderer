# -*- coding: utf-8 -*-
from srmath import *

class VertexShader(object):
	def __init__(self):
		self.outpos = None

	def run(self):
		raise NotImplementedError

