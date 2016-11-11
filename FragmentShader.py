# -*- coding: utf-8 -*-
from color import *

class FragmentShader(object):
	def __init__(self):
		self.color = None

	def run(self):
		raise NotImplementedError

class SimpleFragmentShader(FragmentShader):
	def __init__(self):
		super(SimpleFragmentShader, self).__init__()
		
	def run(self):
		self.color = Color.RED
	


