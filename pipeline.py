# -*- coding: utf-8 -*-
import cube
import srmath
WINDOW_HEIGHT = 512
WINDOW_WIDTH = 512
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
clearColor = BLACK
frameBuffer = [BLACK] * (WINDOW_HEIGHT * WINDOW_WIDTH)
depthBuffer = [1.0] * (WINDOW_HEIGHT * WINDOW_WIDTH)
cameraPosition = srmath.vec3(4, 4, 4)
lookAt = srmath.vec3(0, 0, 0)
cameraAspectRatio = 1.0
cameraFOV = 60
cameraNearPlane = 1.0
cameraFarPlane = 500.0

class DrawMode(object):
	WIRE_FRAME = 1
	VERTEX_COLOR = 2

class SpaceType(object):
	WORLD_SPACE = 1
	VIEW_SPACE = 2

class VertexInput(object):
	def __init__(self):
		self.pos = None
		self.color = None

class VertexAttribute(object):
	def __init__(self):
		self.screenCoord = None
		self.interpolateParam = 0.0
		self.color = BLACK


#called by main window once per frame
def update():
	draw_cube(2.0, color=RED)

def move_camera(offset, space = SpaceType.VIEW_SPACE):
	global cameraPosition
	global lookAt
	if space == SpaceType.VIEW_SPACE:
		invViewMat = srmath.make_inv_view_mat(cameraPosition, lookAt, srmath.vec3(0, 1, 0))
		if not isinstance(offset, srmath.vec4):
			offset = srmath.vec4(offset.x, offset.y, offset.z, 0.0)
		offsetInWorld = invViewMat * offset
		offsetInWorld = srmath.vec3(offsetInWorld.x, offsetInWorld.y, offsetInWorld.z)
		cameraPosition += offsetInWorld
		lookAt += offsetInWorld
	elif space == SpaceType.WORLD_SPACE:
		cameraPosition += offset
		lookAt += offset


def clear_screen():
	global frameBuffer
	frameBuffer = [clearColor] * (WINDOW_HEIGHT * WINDOW_WIDTH)


def draw_point(x, y, color):
	coord = y * WINDOW_WIDTH + x
	if 0 <= coord < len(frameBuffer):
		frameBuffer[coord] = color

def draw_line(x0, y0, x1, y1, color):
	if x0 == x1 and y0 == y1:
		#single point
		draw_point(x0, y0, color)
	elif x0 == x1:
		#vertical line
		step = 1 if y1 > y0 else -1
		for y in xrange(y0, y1, step):
			draw_point(x0, y, color)
		draw_point(x1, y1, color)
	elif y0 == y1:
		#horizontal line
		step = 1 if x1 > x0 else -1
		for x in xrange(x0, x1, step):
			draw_point(x, y0, color)
		draw_point(x1, y1, color)
	else:
		delta_x = x0 - x1 if x0 > x1 else x1 - x0
		delta_y = y0 - y1 if y0 > y1 else y1 - y0
		error_term = 0
		if delta_x > delta_y:
			step = 1 if x1 > x0 else -1
			y = y0
			for x in xrange(x0, x1, step):
				draw_point(x, y, color)
				error_term += delta_y
				if error_term >= delta_x:
					error_term -= delta_x
					y += 1 if y1 > y0 else -1
					draw_point(x, y, color)
			draw_point(x1, y1, color)
		else:
			step = 1 if y1 > y0 else -1
			x = x0
			for y in xrange(y0, y1, step):
				draw_point(x, y, color)
				error_term += delta_x
				if error_term >= delta_y:
					error_term -= delta_y
					x += 1 if x1 > x0 else -1
					draw_point(x, y, color)
			draw_point(x1, y1, color)

def draw_triangle_wireframe(v0, v1, v2, color):
	draw_line(int(v0.screenCoord.x), int(v0.screenCoord.y), int(v1.screenCoord.x), int(v1.screenCoord.y), color)
	draw_line(int(v1.screenCoord.x), int(v1.screenCoord.y), int(v2.screenCoord.x), int(v2.screenCoord.y), color)
	draw_line(int(v2.screenCoord.x), int(v2.screenCoord.y), int(v0.screenCoord.x), int(v0.screenCoord.y), color)
	
def draw_triangle(v0, v1, v2, mode, color):
	if mode == DrawMode.WIRE_FRAME:
		draw_triangle_wireframe(v0, v1, v2, color)

def calc_vertex_attribute(mvp, vertexInput):
	vertex = VertexAttribute()
	vertex.screenCoord = mvp * vertexInput.pos
	vertex.interpolateParam = 1.0 / vertex.screenCoord.w
	vertex.screenCoord *= vertex.interpolateParam
	vertex.screenCoord = srmath.ndc_to_screen_coord(vertex.screenCoord, WINDOW_WIDTH, WINDOW_HEIGHT)
	vertex.color = vertexInput.color
	return vertex

def draw_cube(size = 1, worldMatrix = srmath.mat4.identity, color = WHITE, mode = DrawMode.WIRE_FRAME):
	c = cube.Cube(size)
	worldMat = worldMatrix
	viewMat = srmath.make_view_mat(cameraPosition, lookAt, srmath.vec3(0, 1, 0))
	projMat = srmath.make_perspect_mat_fov(cameraAspectRatio, cameraNearPlane, \
			cameraFarPlane, cameraFOV)
	mvp = projMat * viewMat * worldMat
	for i in xrange(0, len(c.indices), 3):
		idx0 = c.indices[i]
		idx1 = c.indices[i + 1]
		idx2 = c.indices[i + 2]
		vsInput0 = VertexInput()
		vsInput0.pos = srmath.vec4(c.vertices[idx0 * 3], c.vertices[idx0 * 3 + 1], \
				c.vertices[idx0 * 3 + 2], 1.0)
		if mode != DrawMode.WIRE_FRAME:
			vsInput0.color = srmath.vec3(c.colors[idx0 * 3], c.colors[idx0 * 3 + 1], c.colors[idx0 * 3 + 2])
		vsInput1 = VertexInput()
		vsInput1.pos = srmath.vec4(c.vertices[idx1 * 3], c.vertices[idx1 * 3 + 1], \
				c.vertices[idx1 * 3 + 2], 1.0)
		if mode != DrawMode.WIRE_FRAME:
			vsInput1.color = srmath.vec3(c.colors[idx1 * 3], c.colors[idx1 * 3 + 1], c.colors[idx1 * 3 + 2])
		vsInput2 = VertexInput()
		vsInput2.pos = srmath.vec4(c.vertices[idx2 * 3], c.vertices[idx2 * 3 + 1], \
				c.vertices[idx2 * 3 + 2], 1.0)
		if mode != DrawMode.WIRE_FRAME:
			vsInput2.color = srmath.vec3(c.colors[idx2 * 3], c.colors[idx2 * 3 + 1], c.colors[idx2 * 3 + 2])
		vertex0 = calc_vertex_attribute(mvp, vsInput0)
		vertex1 = calc_vertex_attribute(mvp, vsInput1)
		vertex2 = calc_vertex_attribute(mvp, vsInput2)
		draw_triangle(vertex0, vertex1, vertex2, mode, color)

