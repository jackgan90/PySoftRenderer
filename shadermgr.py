# -*- coding: utf-8 -*-
import program
import shader

_instance = None

def get_shader_mgr():
	global _instance
	if _instance is None:
		_instance = ShaderMgr()
	return _instance

class ShaderMgr(object):
	def __init__(self):
		pass

	def create_program(self):
		return program.Program()

	def create_shader(self, name):
		shaderClass = getattr(shader, name, None)
		if not shaderClass:
			return None
		else:
			return shaderClass()
