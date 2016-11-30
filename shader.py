# -*- coding: utf-8 -*-
import pipeline
import srmath

class Shader(object):
	def __init__(self):
		super(Shader, self).__init__()
		self.varyings = []
		self.uniforms = []

	def sample_texture(self, tex, uv):
		return pipeline.get_pipeline().sample_texture(tex, uv)

	def set_uniform(self, name, value):
		if name in self.uniforms:
			setattr(self, name, value)

	def set_varying(self, name, value):
		if name in self.varyings:
			setattr(self, name, value)

class VertexShader(Shader):
	def __init__(self):
		super(VertexShader, self).__init__()
		self.varyings = ['position', ]
		self.uniforms = ['mvp', ]
		#input varyings
		self.vspos = None
		self.vsattrs = dict()
	
	def run(self):
		self.vspos = self.mvp * self.position

class FragmentShader(Shader):
	def __init__(self):
		super(FragmentShader, self).__init__()
		self.fragcolor = srmath.vec4()

	def run(self):
		pass

class VertexColorVS(VertexShader):
	def __init__(self):
		super(VertexColorVS, self).__init__()
		self.varyings = ['position', 'color', ]

	def run(self):
		super(VertexColorVS, self).run()
		self.vsattrs['color'] = self.color

class VertexColorFS(FragmentShader):
	def __init__(self):
		super(VertexColorFS, self).__init__()
		self.varyings = ['color', ]

	def run(self):
		self.fragcolor = self.color

class TextureVS(VertexShader):
	def __init__(self):
		super(TextureVS, self).__init__()
		self.varyings = ['position', 'uv', 'color']

	def run(self):
		super(TextureVS, self).run()
		self.vsattrs['uv'] = self.uv
		self.vsattrs['color'] = self.color

class TextureFS(FragmentShader):
	def __init__(self):
		super(TextureFS, self).__init__()
		self.varyings = ['uv', 'color', ]
		self.uniforms = ['texChessboard', ]

	def run(self):
		texColor = self.sample_texture(self.texChessboard, self.uv)
		self.fragcolor = srmath.vec3(texColor.x * self.color.x, texColor.y * self.color.y, texColor.z * self.color.z)


