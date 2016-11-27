# -*- coding: utf-8 -*-

class FragmentProcessor(object):
	def __init__(self, pipeline):
		self.pipeline = pipeline

	def process(self, rasterData, program):
		#don't need to use predifined semantics,because vertex shader already
		#produces what fragment shader needs
		for uniform in program.fs.uniforms:
			if self.pipeline.has_pipeline_uniform(uniform):
				program.fs.set_uniform(uniform, self.pipeline.get_pipeline_uniform(uniform))

		for varyingName, attr in rasterData.fragmentAttrs.iteritems():
			if varyingName in program.fs.varyings:
				program.fs.set_varying(varyingName, attr / rasterData.interpolateParam)

		program.fs.run()
		return program.fs.fragcolor


