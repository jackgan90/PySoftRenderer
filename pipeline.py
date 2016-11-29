# -*- coding: utf-8 -*-
import srmath
import color
import buffer3d
from rasterizer import Rasterizer
from vertexprocessor import VertexProcessor
from  fragmentprocessor import FragmentProcessor

DEFAULT_WINDOW_HEIGHT = 400
DEFAULT_WINDOW_WIDTH = 400

_pipelineInstance = None

def get_pipeline():
	global _pipelineInstance
	if _pipelineInstance is None:
		_pipelineInstance = Pipeline()
	return _pipelineInstance

class DrawMode(object):
	WIRE_FRAME = 1
	FILL = 2

class VertexInput(object):
	def __init__(self):
		self.pos = None
		self.color = None
		self.uv = None

class RasterizeInput(object):
	def __init__(self):
		self.screenCoord = None
		self.interpolateParam = 0.0
		self.color = color.BLACK
		self.uv = srmath.vec2()

class Pipeline(object):
	def __init__(self):
		self.clearColor = color.GREY
		self.frameBuffer = None
		self.depthBuffer = None
		self.vertexProcessor = None
		self.fragmentProcessor = None
		self.rasterizer = None
		#different window system has different pixel binding
		#to boost performance(avoid copying framebuffer)
		#expose an interface to manipulate window specific frame buffer
		self.uniformCache = dict()

	def init(self):
		self.frameBuffer = buffer3d.Buffer3D(DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT, self.clearColor)
		self.depthBuffer = buffer3d.Buffer3D(DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT, 1.0)
		self.vertexProcessor = VertexProcessor(self)
		self.fragmentProcessor = FragmentProcessor(self)
		self.rasterizer = Rasterizer(self)

	def clear_screen(self):
		self.frameBuffer.set_all_value(self.clearColor)

	def clear_depth_buffer(self):
		self.depthBuffer.set_all_value(1.0)

	def get_frame_buffer_dimension(self):
		return (self.frameBuffer.width, self.frameBuffer.height)

	def get_frame_buffer_data(self):
		return self.frameBuffer.data

	def has_pipeline_uniform(self, uniform):
		return uniform in self.uniformCache

	def get_pipeline_uniform(self, uniform):
		return self.uniformCache.get(uniform, None)

	def sample_texture(self, tex, uv):
		x = int(srmath.clamp(srmath.clamp(uv.x, 0.0, 1.0) * tex.width, 0, tex.width - 1))
		y = int(srmath.clamp(srmath.clamp(uv.y, 0.0, 1.0) * tex.height, 0, tex.height - 1))
		return tex.get_value(x, y)

	def set_front_face(self, face):
		self.rasterizer.set_front_face(face)

	def get_pixel(self, x, y):
		return self.frameBuffer.get_value(x, y, self.clearColor)

	def set_pixel(self, x, y, color):
		self.frameBuffer.put_value(x, y, color)

	def get_depth(self, x, y):
		return self.depthBuffer.get_value(x, y, 1.0)

	def set_depth(self, x, y, value):
		self.depthBuffer.put_value(x, y, value)

	def draw_mesh(self, mesh, cam, program, worldMat = srmath.mat4.identity, wireframeColor = color.WHITE, mode = DrawMode.WIRE_FRAME):
		viewMat = cam.get_world_to_view_mat()
		projMat = cam.get_projection_mat()
		mvp = projMat * viewMat * worldMat
		self.uniformCache['world_matrix'] = worldMat
		self.uniformCache['view_matrix'] = viewMat
		self.uniformCache['projection_matrix'] = projMat
		self.uniformCache['mvp'] = mvp
		for i in xrange(0, len(mesh.indices), 3):
			rasterInputs = self.vertexProcessor.process(mesh, mesh.indices[i : i + 3], program)
			self.rasterizer.process(rasterInputs, mode, wireframeColor, program)

