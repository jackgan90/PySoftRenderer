# -*- coding: utf-8 -*-
from srmath import *

class Camera(object):
	def __init__(self):
		self.position = vec3()
		self.up = vec3(0, 1, 0)
		self.lookAt = vec3(0, 0, -1)
