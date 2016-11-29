# -*- coding: utf-8 -*-

class FragmentProcessor(object):
	def __init__(self, pipeline):
		self.pipeline = pipeline

	def process(self, rasterData, program):
		#don't need to use predifined semantics,because vertex shader already
		#produces what fragment shader needs
		fs = program.fs.__class__()
		for uniform in program.fs.uniforms:
			fs.set_uniform(uniform, getattr(program.fs, uniform, None))
		for uniform in fs.uniforms:
			if self.pipeline.has_pipeline_uniform(uniform):
				fs.set_uniform(uniform, self.pipeline.get_pipeline_uniform(uniform))

		for varyingName, attr in rasterData.fragmentAttrs.iteritems():
			if varyingName in fs.varyings:
				fs.set_varying(varyingName, attr / rasterData.interpolateParam)

		fs.run()
		return fs.fragcolor


