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
	draw_cube(2.0, color=RED, mode=DrawMode.VERTEX_COLOR)

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

def clear_depth_buffer():
	global depthBuffer
	depthBuffer = [1.0] * (WINDOW_HEIGHT * WINDOW_WIDTH)



def draw_point(x, y, color):
	coord = y * WINDOW_WIDTH + x
	if 0 <= coord < len(frameBuffer):
		frameBuffer[coord] = color

def get_depth(x, y):
	return depthBuffer[y * WINDOW_WIDTH + x]

def set_depth(x, y, value):
	coord = y * WINDOW_WIDTH + x
	depthBuffer[coord] = value


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
	elif mode == DrawMode.VERTEX_COLOR:
		flatTriangles = get_flat_triangles(v0, v1, v2)
		for v0, v1, v2 in flatTriangles:
			draw_flat_triangle(v0, v1, v2)

def calc_vertex_attribute(mvp, vertexInput, mode):
	vertex = VertexAttribute()
	vertex.screenCoord = mvp * vertexInput.pos
	vertex.interpolateParam = 1.0 / vertex.screenCoord.w
	#perspective division
	vertex.screenCoord *= vertex.interpolateParam
	vertex.screenCoord = srmath.ndc_to_screen_coord(vertex.screenCoord, WINDOW_WIDTH, WINDOW_HEIGHT)
	#invert the interpolate param because we use right-hand coordinate system
	if mode != DrawMode.WIRE_FRAME:
		vertex.color = srmath.vec3(vertexInput.color[0] * vertex.interpolateParam, \
				vertexInput.color[1] * vertex.interpolateParam, vertexInput.color[2] * vertex.interpolateParam)
	return vertex

def interpolateVertex(v0, v1, t):
	vertex = VertexAttribute()
	vertex.interpolateParam = srmath.lerp(v0.interpolateParam, v1.interpolateParam, t)
	vertex.color = srmath.lerp(v0.color, v1.color, t)
	vertex.screenCoord = srmath.lerp(v0.screenCoord, v1.screenCoord, t)
	return vertex

def inBound(x, y):
	return 0 <= x < WINDOW_WIDTH and 0 <= y < WINDOW_HEIGHT

def draw_scanline(left, right):
	xStart = int(left.screenCoord.x)
	xEnd = int(right.screenCoord.x)
	if xStart == xEnd:
		c = left.color / left.interpolateParam
		color = (int(255 * c.x) % 256, int(255 * c.y) % 256, int(255 * c.z) % 256)
		draw_point(int(left.screenCoord.x), int(left.screenCoord.y), color)
		return
		
	y = int(left.screenCoord.y)
	currentVertex = left
	for x in xrange(xStart, xEnd + 1, 1):
		if inBound(x, y):
			depthInBuffer = get_depth(x, y)
			if currentVertex.screenCoord.z <= depthInBuffer:
				set_depth(x, y, currentVertex.screenCoord.z)
				r = int(255 * currentVertex.color.x / currentVertex.interpolateParam) % 256
				g = int(255 * currentVertex.color.y / currentVertex.interpolateParam) % 256
				b = int(255 * currentVertex.color.z / currentVertex.interpolateParam) % 256
				draw_point(x, y, (r, g, b))
		currentVertex = interpolateVertex(left, right, (x + 1 - xStart) / (xEnd - xStart))

def draw_flat_triangle(v0, v1, v2):
	if int(v0.screenCoord.x) == int(v1.screenCoord.x) and int(v0.screenCoord.y) == int(v1.screenCoord.y) \
			and int(v1.screenCoord.x) == int(v2.screenCoord.x) and int(v1.screenCoord.y) == int(v2.screenCoord.y):
		#single point
		c = v0.color / v0.interpolateParam
		color = (int(255 * c.x) % 256, int(255 * c.y) % 256, int(255 * c.z) % 256)
		draw_point(int(v0.screenCoord.x), int(v0.screenCoord.y), color)
	elif int(v0.screenCoord.y) == int(v1.screenCoord.y):
		if v0.screenCoord.x < v1.screenCoord.x:
			left = v0
			right = v1
		else:
			left = v1
			right = v0
		bottom = v2
		yStart = left.screenCoord.y
		yEnd = bottom.screenCoord.y
		for y in xrange(int(yStart), int(yEnd) + 1, 1):
			interpolateLeft = interpolateVertex(left, bottom, (y - yStart) / (yEnd - yStart))
			interpolateRight = interpolateVertex(right, bottom, (y - yStart) / (yEnd - yStart))
			draw_scanline(interpolateLeft, interpolateRight)
	elif int(v1.screenCoord.y) == int(v2.screenCoord.y):
		if v1.screenCoord.x < v2.screenCoord.x:
			left = v1
			right = v2
		else:
			left = v2
			right = v1
		top = v0
		yStart = v0.screenCoord.y
		yEnd = left.screenCoord.y
		for y in xrange(int(yStart), int(yEnd) + 1, 1):
			interpolateLeft = interpolateVertex(top, left, (y - yStart) / (yEnd - yStart))
			interpolateRight = interpolateVertex(top, right, (y - yStart) / (yEnd - yStart))
			draw_scanline(interpolateLeft, interpolateRight)
	else:
		print '-' * 30
		print v0.screenCoord, v1.screenCoord, v2.screenCoord
		print '-' * 30
		raise Exception('draw_flat_triangle should only handle flat triangle!')

def get_flat_triangles(v0, v1, v2):
	triList = [v0, v1, v2]
	triList.sort(key = lambda x : x.screenCoord.y)
	if v0.screenCoord.y == v1.screenCoord.y or \
		v1.screenCoord.y == v2.screenCoord.y:
		return ((triList[0], triList[1], triList[2]), )
	else:
		t = (triList[1].screenCoord.y - triList[0].screenCoord.y) / (triList[2].screenCoord.y - triList[0].screenCoord.y)
		v3 = interpolateVertex(triList[0], triList[2], t)
		return ((triList[0], triList[1], v3, ), (v3, triList[1], triList[2], ), )

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
		vertex0 = calc_vertex_attribute(mvp, vsInput0, mode)
		vertex1 = calc_vertex_attribute(mvp, vsInput1, mode)
		vertex2 = calc_vertex_attribute(mvp, vsInput2, mode)
		draw_triangle(vertex0, vertex1, vertex2, mode, color)

