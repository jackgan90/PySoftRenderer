# -*- coding: utf-8 -*-
import srmath
import color
import texture
import buffer3d

DEFAULT_WINDOW_HEIGHT = 400
DEFAULT_WINDOW_WIDTH = 400

_pipelineInstance = None

def get_pipeline():
	global _pipelineInstance
	if _pipelineInstance is None:
		_pipelineInstance = Pipeline()
	return _pipelineInstance

class WindingOrder(object):
	CW = 1
	CCW = 2

class DrawMode(object):
	WIRE_FRAME = 1
	VERTEX_COLOR = 2
	TEXTURE_MAP = 3

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
		self.textures = []
		self.frontFace = WindingOrder.CCW

	def init(self):
		self.frameBuffer = buffer3d.Buffer3D(DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT, self.clearColor)
		self.depthBuffer = buffer3d.Buffer3D(DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT, 1.0)

	def clear_screen(self):
		self.frameBuffer.set_all_value(self.clearColor)

	def clear_depth_buffer(self):
		self.depthBuffer.set_all_value(1.0)

	def set_front_face(self, face):
		self.frontFace = face

	def sample_texture(self, tex, uv):
		x = int(srmath.clamp(srmath.clamp(uv.x, 0.0, 1.0) * tex.width, 0, tex.width - 1))
		y = int(srmath.clamp(srmath.clamp(uv.y, 0.0, 1.0) * tex.height, 0, tex.height - 1))
		return tex.get_value(x, y)

	def get_pixel(self, x, y):
		return self.frameBuffer.get_value(x, y, self.clearColor)

	def draw_point(self, x, y, color):
		self.frameBuffer.put_value(x, y, color)

	def get_depth(self, x, y):
		return self.depthBuffer.get_value(x, y, 1.0)

	def set_depth(self, x, y, value):
		self.depthBuffer.put_value(x, y, value)

	def draw_line(self, x0, y0, x1, y1, color):
		if x0 == x1 and y0 == y1:
			#single point
			self.draw_point(x0, y0, color)
		elif x0 == x1:
			#vertical line
			step = 1 if y1 > y0 else -1
			for y in xrange(y0, y1, step):
				self.draw_point(x0, y, color)
			self.draw_point(x1, y1, color)
		elif y0 == y1:
			#horizontal line
			step = 1 if x1 > x0 else -1
			for x in xrange(x0, x1, step):
				self.draw_point(x, y0, color)
			self.draw_point(x1, y1, color)
		else:
			delta_x = x0 - x1 if x0 > x1 else x1 - x0
			delta_y = y0 - y1 if y0 > y1 else y1 - y0
			error_term = 0
			if delta_x > delta_y:
				step = 1 if x1 > x0 else -1
				y = y0
				for x in xrange(x0, x1, step):
					self.draw_point(x, y, color)
					error_term += delta_y
					if error_term >= delta_x:
						error_term -= delta_x
						y += 1 if y1 > y0 else -1
						self.draw_point(x, y, color)
				self.draw_point(x1, y1, color)
			else:
				step = 1 if y1 > y0 else -1
				x = x0
				for y in xrange(y0, y1, step):
					self.draw_point(x, y, color)
					error_term += delta_x
					if error_term >= delta_y:
						error_term -= delta_y
						x += 1 if x1 > x0 else -1
						self.draw_point(x, y, color)
				self.draw_point(x1, y1, color)

	def draw_triangle_wireframe(self, v0, v1, v2, color):
		self.draw_line(int(v0.screenCoord.x), int(v0.screenCoord.y), int(v1.screenCoord.x), int(v1.screenCoord.y), color)
		self.draw_line(int(v1.screenCoord.x), int(v1.screenCoord.y), int(v2.screenCoord.x), int(v2.screenCoord.y), color)
		self.draw_line(int(v2.screenCoord.x), int(v2.screenCoord.y), int(v0.screenCoord.x), int(v0.screenCoord.y), color)
		
	def draw_triangle(self, v0, v1, v2, mode, color):
		if mode == DrawMode.WIRE_FRAME:
			self.draw_triangle_wireframe(v0, v1, v2, color)
		elif mode in (DrawMode.VERTEX_COLOR, DrawMode.TEXTURE_MAP):
			flatTriangles = self.get_flat_triangles(v0, v1, v2)
			for vertex0, vertex1, vertex2 in flatTriangles:
				self.draw_flat_triangle(vertex0, vertex1, vertex2, mode)

	def calc_vertex_attribute(self, mvp, vertexInput, mode):
		rInput = RasterizeInput()
		rInput.screenCoord = mvp * vertexInput.pos
		rInput.interpolateParam = 1.0 / rInput.screenCoord.w
		#perspective division
		rInput.screenCoord *= rInput.interpolateParam
		rInput.screenCoord = srmath.ndc_to_screen_coord(rInput.screenCoord, self.frameBuffer.width, self.frameBuffer.height)
		if mode != DrawMode.WIRE_FRAME:
			rInput.color = srmath.vec3(vertexInput.color[0] * rInput.interpolateParam, \
					vertexInput.color[1] * rInput.interpolateParam, vertexInput.color[2] * rInput.interpolateParam)
		if mode == DrawMode.TEXTURE_MAP:
			rInput.uv = vertexInput.uv * rInput.interpolateParam
		return rInput

	def interpolate_rasterize_input(self, v0, v1, t):
		rInput = RasterizeInput()
		rInput.interpolateParam = srmath.lerp(v0.interpolateParam, v1.interpolateParam, t)
		rInput.color = srmath.lerp(v0.color, v1.color, t)
		rInput.screenCoord = srmath.lerp(v0.screenCoord, v1.screenCoord, t)
		rInput.uv = srmath.lerp(v0.uv, v1.uv, t)
		return rInput

	def draw_scanline(self, left, right, y, mode):
		xStart = int(left.screenCoord.x)
		xEnd = int(right.screenCoord.x + 1)
		currentVertex = left
		for x in xrange(xStart, xEnd, 1):
			if 0 <= x < self.frameBuffer.width and 0 <= y < self.frameBuffer.height:
				depthInBuffer = self.get_depth(x, y)
				if currentVertex.screenCoord.z < depthInBuffer:
					self.set_depth(x, y, currentVertex.screenCoord.z)
					if mode == DrawMode.VERTEX_COLOR:
						r = int(255 * currentVertex.color.x / currentVertex.interpolateParam) % 256
						g = int(255 * currentVertex.color.y / currentVertex.interpolateParam) % 256
						b = int(255 * currentVertex.color.z / currentVertex.interpolateParam) % 256
					elif mode == DrawMode.TEXTURE_MAP:
						tex = self.textures[0]
						uv = currentVertex.uv / currentVertex.interpolateParam
						r, g, b = self.sample_texture(tex, uv)
					self.draw_point(x, y, (r, g, b))
			currentVertex = self.interpolate_rasterize_input(left, right, float(x + 1 - xStart) / (xEnd - xStart))

	def draw_flat_triangle(self, v0, v1, v2, mode):
		if int(v0.screenCoord.y) == int(v1.screenCoord.y) and int(v1.screenCoord.y) == int(v2.screenCoord.y):
			left = v0 if v0.screenCoord.x < v1.screenCoord.x else v1
			left = left if left.screenCoord.x < v2.screenCoord.x else v2
			right = v0 if v0.screenCoord.x > v1.screenCoord.x else v1
			right = right if right.screenCoord.x > v2.screenCoord.x else v2
			self.draw_scanline(left, right, int(v0.screenCoord.y), mode)
			#single point
		elif int(v0.screenCoord.y) == int(v1.screenCoord.y):
			if v0.screenCoord.x < v1.screenCoord.x:
				left = v0
				right = v1
			else:
				left = v1
				right = v0
			bottom = v2
			yStart = int(left.screenCoord.y)
			yEnd = int(bottom.screenCoord.y)
			if yStart == yEnd:
				self.draw_scanline(left, right, yStart, mode)
				return
			for y in xrange(yStart, yEnd + 1, 1):
				interpolateLeft = self.interpolate_rasterize_input(left, bottom, float(y - yStart) / (yEnd - yStart))
				interpolateRight = self.interpolate_rasterize_input(right, bottom, float(y - yStart) / (yEnd - yStart))
				self.draw_scanline(interpolateLeft, interpolateRight, y, mode)
		elif int(v1.screenCoord.y) == int(v2.screenCoord.y):
			if v1.screenCoord.x < v2.screenCoord.x:
				left = v1
				right = v2
			else:
				left = v2
				right = v1
			top = v0
			yStart = int(v0.screenCoord.y)
			yEnd = int(left.screenCoord.y)
			if yStart == yEnd:
				self.draw_scanline(left, right, yStart, mode)
				return
			for y in xrange(yStart, yEnd + 1, 1):
				interpolateLeft = self.interpolate_rasterize_input(top, left, float(y - yStart) / (yEnd - yStart))
				interpolateRight = self.interpolate_rasterize_input(top, right, float(y - yStart) / (yEnd - yStart))
				self.draw_scanline(interpolateLeft, interpolateRight, y, mode)
		else:
			raise Exception('draw_flat_triangle should only handle flat triangle!')

	def get_flat_triangles(self, v0, v1, v2):
		triList = [v0, v1, v2]
		triList.sort(key = lambda x : x.screenCoord.y)
		if int(triList[0].screenCoord.y) == int(triList[1].screenCoord.y) or \
			int(triList[1].screenCoord.y) == int(triList[2].screenCoord.y):
			return ((triList[0], triList[1], triList[2]), )
		else:
			t = (triList[1].screenCoord.y - triList[0].screenCoord.y) / (triList[2].screenCoord.y - triList[0].screenCoord.y)
			v3 = self.interpolate_rasterize_input(triList[0], triList[2], t)
			return ((triList[0], triList[1], v3, ), (v3, triList[1], triList[2], ), )

	def cull_back_face(self, v0, v1, v2):
		dir0 = v1.screenCoord - v0.screenCoord
		dir1 = v2.screenCoord - v1.screenCoord
		dir0.z = 0
		dir1.z = 0
		product = dir0.cross(dir1)
		isClockwise = product.z > 0
		if isClockwise and self.frontFace == WindingOrder.CCW:
			return True
		elif not isClockwise and self.frontFace == WindingOrder.CW:
			return True
		else:
			return False

	def draw_mesh(self, mesh, cam, worldMatrix = srmath.mat4.identity, wireframeColor = color.WHITE, mode = DrawMode.WIRE_FRAME):
		viewMat = cam.get_world_to_view_mat()
		projMat = cam.get_projection_mat()
		mvp = projMat * viewMat * worldMatrix
		if mode == DrawMode.TEXTURE_MAP and not self.textures:
			tex = texture.create_chess_board_texture(self.frameBuffer.width, self.frameBuffer.height, \
					(20, 160, 135), (160, 204, 20))
			self.textures.append(tex)
		for i in xrange(0, len(mesh.indices), 3):
			idx0 = mesh.indices[i]
			idx1 = mesh.indices[i + 1]
			idx2 = mesh.indices[i + 2]
			vsInput0 = VertexInput()
			vsInput0.pos = srmath.vec4(mesh.vertices[idx0 * 3], mesh.vertices[idx0 * 3 + 1], \
					mesh.vertices[idx0 * 3 + 2], 1.0)
			if mode != DrawMode.WIRE_FRAME:
				vsInput0.color = srmath.vec3(mesh.colors[idx0 * 3], mesh.colors[idx0 * 3 + 1], mesh.colors[idx0 * 3 + 2])
			if mode == DrawMode.TEXTURE_MAP:
				vsInput0.uv = srmath.vec2(mesh.uvs[idx0 * 3], mesh.uvs[idx0 * 3 + 1])
			vsInput1 = VertexInput()
			vsInput1.pos = srmath.vec4(mesh.vertices[idx1 * 3], mesh.vertices[idx1 * 3 + 1], \
					mesh.vertices[idx1 * 3 + 2], 1.0)
			if mode != DrawMode.WIRE_FRAME:
				vsInput1.color = srmath.vec3(mesh.colors[idx1 * 3], mesh.colors[idx1 * 3 + 1], mesh.colors[idx1 * 3 + 2])
			if mode == DrawMode.TEXTURE_MAP:
				vsInput1.uv = srmath.vec2(mesh.uvs[idx1 * 3], mesh.uvs[idx1 * 3 + 1])
			vsInput2 = VertexInput()
			vsInput2.pos = srmath.vec4(mesh.vertices[idx2 * 3], mesh.vertices[idx2 * 3 + 1], \
					mesh.vertices[idx2 * 3 + 2], 1.0)
			if mode != DrawMode.WIRE_FRAME:
				vsInput2.color = srmath.vec3(mesh.colors[idx2 * 3], mesh.colors[idx2 * 3 + 1], mesh.colors[idx2 * 3 + 2])
			if mode == DrawMode.TEXTURE_MAP:
				vsInput2.uv = srmath.vec2(mesh.uvs[idx2 * 3], mesh.uvs[idx2 * 3 + 1])
			vertex0 = self.calc_vertex_attribute(mvp, vsInput0, mode)
			vertex1 = self.calc_vertex_attribute(mvp, vsInput1, mode)
			vertex2 = self.calc_vertex_attribute(mvp, vsInput2, mode)
			if self.cull_back_face(vertex0, vertex1, vertex2):
				continue
			self.draw_triangle(vertex0, vertex1, vertex2, mode, wireframeColor)

