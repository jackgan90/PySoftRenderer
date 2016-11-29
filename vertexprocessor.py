# -*- coding: utf-8 -*-
from rasterizer import RasterizeInput  
import srmath

class VertexProcessor(object):
	def __init__(self, pipeline):
		self.pipeline = pipeline

	def process(self, mesh, indices, program, mode, wireframeColor):
		rasterInputs = []
		for idx in indices:
			# variable semantics are predifined,position is always coordinate in object space
			# color is vertex color
			# uv is vertex texture coordinate
			vs = program.vs.__class__()
			for uniform in program.vs.uniforms:
				vs.set_uniform(uniform, getattr(program.vs, uniform, None))
			if 'position' in vs.varyings:
				position = srmath.vec4(mesh.vertices[idx * 3], mesh.vertices[idx * 3 + 1], \
						mesh.vertices[idx * 3 + 2], 1.0)
				vs.set_varying('position', position)
			if 'color' in vs.varyings:
				color = srmath.vec3(mesh.colors[idx * 3], mesh.colors[idx * 3 + 1], mesh.colors[idx * 3 + 2])
				vs.set_varying('color', color)
			if 'uv' in vs.varyings:
				uv = srmath.vec2(mesh.uvs[idx * 3], mesh.uvs[idx * 3 + 1])
				vs.set_varying('uv', uv)

			for uniform in vs.uniforms:
				if self.pipeline.has_pipeline_uniform(uniform):
					vs.set_uniform(uniform, self.pipeline.get_pipeline_uniform(uniform))
			
			vs.run()
			rasterInput = RasterizeInput()
			rasterInput.clipPos = srmath.vec4(vs.vspos.x, vs.vspos.y, \
					vs.vspos.z, vs.vspos.w)
			rasterInput.vertexAttrs = dict(vs.vsattrs)
			rasterInputs.append(rasterInput)
		self.pipeline.triangleProcessQueue.put({'rasterInputs' : rasterInputs, 'mode' : mode, 'wireframeColor' : wireframeColor, 'program' : program})
