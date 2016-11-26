# -*- coding: utf-8 -*-
import srmath
import color
import texture
import buffer3d

WINDOW_HEIGHT = 400
WINDOW_WIDTH = 400

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

clearColor = color.GREY
frameBuffer = buffer3d.Buffer3D(WINDOW_WIDTH, WINDOW_HEIGHT, clearColor)
depthBuffer = buffer3d.Buffer3D(WINDOW_WIDTH, WINDOW_HEIGHT, 1.0)
textures = []
frontFace = WindingOrder.CCW


def clear_screen():
	global frameBuffer
	frameBuffer.set_all_value(clearColor)

def clear_depth_buffer():
	global depthBuffer
	depthBuffer.set_all_value(1.0)

def set_front_face(face):
	global frontFace
	frontFace = face

def create_chess_board_texture(w = WINDOW_WIDTH, h = WINDOW_HEIGHT, cells = 5):
	tex = texture.Texture(w, h)
	cellWidth = w / cells
	cellHeight = h / cells
	for x in xrange(w):
		for y in xrange(h):
			tex.buffer.append((20, 160, 135) if x / cellWidth % 2 == 0  and y / cellHeight % 2 == 0 else (160, 204, 20))
	textures.append(tex)
	return tex

def sample_texture(tex, uv):
	x = int(srmath.clamp(srmath.clamp(uv.x, 0.0, 1.0) * tex.width, 0, tex.width - 1))
	y = int(srmath.clamp(srmath.clamp(uv.y, 0.0, 1.0) * tex.height, 0, tex.height - 1))
	return tex.buffer[y * tex.width + x]

def get_pixel(x, y):
	if x < 0 or x >= WINDOW_WIDTH:
		return clearColor
	if y < 0 or y >= WINDOW_HEIGHT:
		return clearColor
	return frameBuffer.get_value(x, y)

def draw_point(x, y, color):
	frameBuffer.put_value(x, y, color)

def get_depth(x, y):
	if x < 0 or x >= WINDOW_WIDTH:
		return 1.0
	if y < 0 or y >= WINDOW_HEIGHT:
		return 1.0
	return depthBuffer.get_value(x, y)

def set_depth(x, y, value):
	global depthBuffer
	depthBuffer.put_value(x, y, value)


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
	elif mode in (DrawMode.VERTEX_COLOR, DrawMode.TEXTURE_MAP):
		flatTriangles = get_flat_triangles(v0, v1, v2)
		for vertex0, vertex1, vertex2 in flatTriangles:
			draw_flat_triangle(vertex0, vertex1, vertex2, mode)

def calc_vertex_attribute(mvp, vertexInput, mode):
	rInput = RasterizeInput()
	rInput.screenCoord = mvp * vertexInput.pos
	rInput.interpolateParam = 1.0 / rInput.screenCoord.w
	#perspective division
	rInput.screenCoord *= rInput.interpolateParam
	rInput.screenCoord = srmath.ndc_to_screen_coord(rInput.screenCoord, WINDOW_WIDTH, WINDOW_HEIGHT)
	#invert the interpolate param because we use right-hand coordinate system
	if mode != DrawMode.WIRE_FRAME:
		rInput.color = srmath.vec3(vertexInput.color[0] * rInput.interpolateParam, \
				vertexInput.color[1] * rInput.interpolateParam, vertexInput.color[2] * rInput.interpolateParam)
	if mode == DrawMode.TEXTURE_MAP:
		rInput.uv = vertexInput.uv * rInput.interpolateParam
	return rInput

def interpolate_rasterize_input(v0, v1, t):
	rInput = RasterizeInput()
	rInput.interpolateParam = srmath.lerp(v0.interpolateParam, v1.interpolateParam, t)
	rInput.color = srmath.lerp(v0.color, v1.color, t)
	rInput.screenCoord = srmath.lerp(v0.screenCoord, v1.screenCoord, t)
	rInput.uv = srmath.lerp(v0.uv, v1.uv, t)
	return rInput

def inBound(x, y):
	return 0 <= x < WINDOW_WIDTH and 0 <= y < WINDOW_HEIGHT

def draw_scanline(left, right, y, mode):
	xStart = int(left.screenCoord.x)
	xEnd = int(right.screenCoord.x + 1)
	# if xStart == xEnd:
		# c = left.color / left.interpolateParam
		# color = (int(255 * c.x) % 256, int(255 * c.y) % 256, int(255 * c.z) % 256)
		# draw_point(xStart, y, color)
		# return
		
	currentVertex = left
	for x in xrange(xStart, xEnd, 1):
		if inBound(x, y):
			depthInBuffer = get_depth(x, y)
			if currentVertex.screenCoord.z < depthInBuffer:
				set_depth(x, y, currentVertex.screenCoord.z)
				if mode == DrawMode.VERTEX_COLOR:
					r = int(255 * currentVertex.color.x / currentVertex.interpolateParam) % 256
					g = int(255 * currentVertex.color.y / currentVertex.interpolateParam) % 256
					b = int(255 * currentVertex.color.z / currentVertex.interpolateParam) % 256
				elif mode == DrawMode.TEXTURE_MAP:
					tex = textures[0]
					uv = currentVertex.uv / currentVertex.interpolateParam
					r, g, b = sample_texture(tex, uv)
					# print r, g, b
				draw_point(x, y, (r, g, b))
		currentVertex = interpolate_rasterize_input(left, right, float(x + 1 - xStart) / (xEnd - xStart))

def draw_flat_triangle(v0, v1, v2, mode):
	if int(v0.screenCoord.y) == int(v1.screenCoord.y) and int(v1.screenCoord.y) == int(v2.screenCoord.y):
		left = v0 if v0.screenCoord.x < v1.screenCoord.x else v1
		left = left if left.screenCoord.x < v2.screenCoord.x else v2
		right = v0 if v0.screenCoord.x > v1.screenCoord.x else v1
		right = right if right.screenCoord.x > v2.screenCoord.x else v2
		draw_scanline(left, right, int(v0.screenCoord.y), mode)
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
			draw_scanline(left, right, yStart, mode)
			return
		for y in xrange(yStart, yEnd + 1, 1):
			interpolateLeft = interpolate_rasterize_input(left, bottom, float(y - yStart) / (yEnd - yStart))
			interpolateRight = interpolate_rasterize_input(right, bottom, float(y - yStart) / (yEnd - yStart))
			draw_scanline(interpolateLeft, interpolateRight, y, mode)
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
			draw_scanline(left, right, yStart, mode)
			return
		for y in xrange(yStart, yEnd + 1, 1):
			interpolateLeft = interpolate_rasterize_input(top, left, float(y - yStart) / (yEnd - yStart))
			interpolateRight = interpolate_rasterize_input(top, right, float(y - yStart) / (yEnd - yStart))
			draw_scanline(interpolateLeft, interpolateRight, y, mode)
	else:
		print '-' * 30
		print v0.screenCoord, v1.screenCoord, v2.screenCoord
		print '-' * 30
		raise Exception('draw_flat_triangle should only handle flat triangle!')

def get_flat_triangles(v0, v1, v2):
	triList = [v0, v1, v2]
	triList.sort(key = lambda x : x.screenCoord.y)
	if int(triList[0].screenCoord.y) == int(triList[1].screenCoord.y) or \
		int(triList[1].screenCoord.y) == int(triList[2].screenCoord.y):
		return ((triList[0], triList[1], triList[2]), )
	else:
		t = (triList[1].screenCoord.y - triList[0].screenCoord.y) / (triList[2].screenCoord.y - triList[0].screenCoord.y)
		v3 = interpolate_rasterize_input(triList[0], triList[2], t)
		return ((triList[0], triList[1], v3, ), (v3, triList[1], triList[2], ), )

def cull_back_face(v0, v1, v2):
	dir0 = v1.screenCoord - v0.screenCoord
	dir1 = v2.screenCoord - v1.screenCoord
	dir0.z = 0
	dir1.z = 0
	product = dir0.cross(dir1)
	isClockwise = product.z > 0
	if isClockwise and frontFace == WindingOrder.CCW:
		return True
	elif not isClockwise and frontFace == WindingOrder.CW:
		return True
	else:
		return False

def draw_mesh(mesh, cam, worldMatrix = srmath.mat4.identity, wireframeColor = color.WHITE, mode = DrawMode.WIRE_FRAME):
	viewMat = cam.get_world_to_view_mat()
	projMat = cam.get_projection_mat()
	mvp = projMat * viewMat * worldMatrix
	if mode == DrawMode.TEXTURE_MAP and not textures:
		create_chess_board_texture()
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
		vertex0 = calc_vertex_attribute(mvp, vsInput0, mode)
		vertex1 = calc_vertex_attribute(mvp, vsInput1, mode)
		vertex2 = calc_vertex_attribute(mvp, vsInput2, mode)
		if cull_back_face(vertex0, vertex1, vertex2):
			continue
		draw_triangle(vertex0, vertex1, vertex2, mode, wireframeColor)
