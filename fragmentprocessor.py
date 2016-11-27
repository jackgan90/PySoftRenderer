# -*- coding: utf-8 -*-

class FragmentProcessor(object):
	def __init__(self, pipeline):
		self.pipeline = pipeline

	def process(self, rasterData, shader):
		#don't need to use predifined semantics,because vertex shader already
		#produces what fragment shader needs
		for uniform in shader.uniforms:
			if self.pipeline.has_pipeline_uniform(uniform):
				shader.set_uniform(uniform, self.pipeline.get_pipeline_uniform(uniform))

		for varyingName, attr in rasterData.fragmentAttrs.iteritems():
			if varyingName in shader.varyings:
				shader.set_varying(varyingName, attr / rasterData.interpolateParam)

		shader.run()
		return shader.fragcolor


