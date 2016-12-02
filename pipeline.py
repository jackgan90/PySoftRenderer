# -*- coding: utf-8 -*-
import srmath
import color
import framebuffer
import depthbuffer
from rasterizer import Rasterizer
from vertexprocessor import VertexProcessor
from  fragmentprocessor import FragmentProcessor
from Queue import Queue
from threading import Thread
import multiprocessing
import config

_pipelineInstance = None

def get_pipeline():
	global _pipelineInstance
	if _pipelineInstance is None:
		_pipelineInstance = Pipeline()
	return _pipelineInstance

class DrawMode(object):
	WIRE_FRAME = 1
	FILL = 2

class RasterizeInput(object):
	def __init__(self):
		self.screenCoord = None
		self.interpolateParam = 0.0
		self.color = color.BLACK
		self.uv = srmath.vec2()

class Pipeline(object):
	def __init__(self):
		self.clearColor = color.GREY
		self.frontBuffer = None
		self.backBuffer = None
		self.depthBuffer = None
		self.vertexProcessor = None
		self.fragmentProcessor = None
		self.rasterizer = None
		self.uniformCache = dict()
		self.cpuCount = multiprocessing.cpu_count()
		self.vertexProcessQueue = Queue()
		self.triangleProcessQueue = Queue()
		self.scanlineDrawQueue = Queue()
		self.quit = False

	def init(self):
		self.frontBuffer = framebuffer.FrameBuffer(config.RESOLUTION[0], config.RESOLUTION[1], self.clearColor)
		self.backBuffer = framebuffer.FrameBuffer(config.RESOLUTION[0], config.RESOLUTION[1], self.clearColor)
		self.depthBuffer = depthbuffer.DepthBuffer(config.RESOLUTION[0], config.RESOLUTION[1], 1.0)
		self.vertexProcessor = VertexProcessor(self)
		self.fragmentProcessor = FragmentProcessor(self)
		self.rasterizer = Rasterizer(self)
		if config.USE_MULTI_THREAD:
			t1 = Thread(target = self.processVertexThread)
			t2 = Thread(target = self.processTriangleThread)
			t1.start()
			t2.start()
			scanlineDrawThreadCnt = self.cpuCount - 3 if self.cpuCount > 3 else 1
			for i in xrange(scanlineDrawThreadCnt):
				t = Thread(target = self.drawScanlineThread)
				t.start()

	def processVertexThread(self):
		while not self.quit:
			task = self.vertexProcessQueue.get()
			mesh = task.get('mesh', None)
			indices = task.get('indices', [])
			program = task.get('program', None)
			mode = task.get('mode', 0)
			wireframeColor = task.get('wireframeColor', color.BLACK)
			if mesh and indices and program:
				self.vertexProcessor.process(mesh, indices, program, mode, wireframeColor)
				self.vertexProcessQueue.task_done()
			else:
				self.vertexProcessQueue.task_done()

	def processTriangleThread(self):
		while not self.quit:
			task = self.triangleProcessQueue.get()
			rasterInputs = task.get('rasterInputs', [])
			mode = task.get('mode', 0)
			wireframeColor = task.get('wireframeColor', color.BLACK)
			program = task.get('program', None)
			if rasterInputs and mode and program:
				self.rasterizer.process(rasterInputs, mode, wireframeColor, program)
				self.triangleProcessQueue.task_done()
			else:
				self.triangleProcessQueue.task_done()

	def drawScanlineThread(self):
		while not self.quit:
			task = self.scanlineDrawQueue.get()
			left = task.get('left', None)
			right = task.get('right', None)
			y = task.get('y', -1)
			mode = task.get('mode', 0)
			program = task.get('program', None)
			if left and right and y >= 0 and mode and program:
				self.rasterizer.draw_scanline(left, right, y, mode, program)
				self.scanlineDrawQueue.task_done()
			else:
				self.scanlineDrawQueue.task_done()

	def clear_screen(self):
		self.backBuffer.set_all_value(self.clearColor)

	def clear_depth_buffer(self):
		self.depthBuffer.set_all_value(1.0)

	def get_frame_buffer_dimension(self):
		return (self.backBuffer.width, self.backBuffer.height)

	def get_frame_buffer_data(self, isBack=False):
		pixelBuffer = self.backBuffer if isBack else self.frontBuffer
		return pixelBuffer.data

	def has_pipeline_uniform(self, uniform):
		return uniform in self.uniformCache

	def get_pipeline_uniform(self, uniform):
		return self.uniformCache.get(uniform, None)

	def sample_texture(self, tex, uv):
		x = int(srmath.clamp(srmath.clamp(uv.x, 0.0, 1.0) * tex.width, 0, tex.width - 1))
		y = int(srmath.clamp(srmath.clamp(uv.y, 0.0, 1.0) * tex.height, 0, tex.height - 1))
		return tex.get_value(x, y)

	def swap_front_back_buffers(self):
		temp = self.frontBuffer
		self.frontBuffer = self.backBuffer
		self.backBuffer = temp

	def set_front_face(self, face):
		self.rasterizer.set_front_face(face)

	def get_pixel(self, x, y, isBack=False):
		pixelBuffer = self.backBuffer if isBack else self.frontBuffer
		return pixelBuffer.get_value(x, y, self.clearColor)

	def set_pixel(self, x, y, color, isBack=True):
		pixelBuffer = self.backBuffer if isBack else self.frontBuffer
		if 0 <= x < pixelBuffer.width and 0 <= y < pixelBuffer.height:
			pixelBuffer.put_value(x, y, color)

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
			if config.USE_MULTI_THREAD:
				self.vertexProcessQueue.put({'mesh' : mesh, 'indices' : mesh.indices[i : i + 3], 'program' : program,
					'mode' : mode, 'wireframeColor' : wireframeColor})
			else:
				rasterInputs = self.vertexProcessor.process(mesh, mesh.indices[i : i + 3], program, mode, wireframeColor)
				self.rasterizer.process(rasterInputs, mode, wireframeColor, program)

		if config.USE_MULTI_THREAD:
			self.vertexProcessQueue.join()
			self.triangleProcessQueue.join()
			self.scanlineDrawQueue.join()

