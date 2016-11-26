# -*- coding: utf-8 -*-
from rasterizer import RasterizeInput  
import srmath

class VertexProcessor(object):
	def __init__(self, pipeline):
		self.pipeline = pipeline

	def process(self, mesh, indices, shader):
		rasterInputs = []
		for idx in indices:
			# variable semantics are predifined,position is always coordinate in object space
			# color is vertex color
			# uv is vertex texture coordinate
			if 'position' in shader.varyings:
				position = srmath.vec4(mesh.vertices[idx * 3], mesh.vertices[idx * 3 + 1], \
						mesh.vertices[idx * 3 + 2], 1.0)
				shader.set_varying('position', position)
			if 'color' in shader.varyings:
				color = srmath.vec3(mesh.colors[idx * 3], mesh.colors[idx * 3 + 1], mesh.colors[idx * 3 + 2])
				shader.set_varying('color', color)
			if 'uv' in shader.varyings:
				uv = srmath.vec2(mesh.uvs[idx * 3], mesh.uvs[idx * 3 + 1])
				shader.set_varying('uv', uv)

			for uniform in shader.uniforms:
				if uniform in self.pipeline.uniformCache:
					shader.set_uniform(uniform, self.pipeline.uniformCache[uniform])
			
			shader.run()
			rasterInput = RasterizeInput()
			rasterInput.clipPos = srmath.vec4(shader.vspos.x, shader.vspos.y, shader.vspos.z, shader.vspos.w)
			rasterInput.vertexAttrs = dict(shader.vsattrs)
			rasterInputs.append(rasterInput)
		return rasterInputs
