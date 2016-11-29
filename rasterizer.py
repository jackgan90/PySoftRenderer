# -*- coding: utf-8 -*-
import srmath
import pipeline

class WindingOrder(object):
	CW = 1
	CCW = 2

class RasterizeInput(object):
	def __init__(self):
		self.clipPos = None
		self.vertexAttrs = dict()

class RasterizeData(object):
	def __init__(self):
		self.screenCoord = None
		self.interpolateParam = 0.0
		self.fragmentAttrs = dict()

class Rasterizer(object):
	def __init__(self, graphicsPipeline):
		self.graphicsPipeline = graphicsPipeline
		self.frontFace = WindingOrder.CCW
		self.width, self.height = self.graphicsPipeline.get_frame_buffer_dimension()

	def set_front_face(self, face):
		self.frontFace = face

	def init_raster_data(self, rasterInput):
		rasterData = RasterizeData()
		rasterData.interpolateParam = 1.0 / rasterInput.clipPos.w
		rasterData.screenCoord = rasterInput.clipPos * rasterData.interpolateParam
		#perspective division
		rasterData.screenCoord = srmath.ndc_to_screen_coord(rasterData.screenCoord, self.width, self.height)
		for varyingName, attr in rasterInput.vertexAttrs.iteritems():
			rasterData.fragmentAttrs[varyingName] = attr * rasterData.interpolateParam

		return rasterData

	def rasterize_triangle(self, rasterDatas, mode, color, program):
		if mode == pipeline.DrawMode.WIRE_FRAME:
			self.rasterize_triangle_wireframe(rasterDatas[0], rasterDatas[1], rasterDatas[2], color)
		else:
			flatTriangles = self.get_flat_triangles(rasterDatas[0], rasterDatas[1], rasterDatas[2])
			for vertex0, vertex1, vertex2 in flatTriangles:
				self.rasterize_flat_triangle(vertex0, vertex1, vertex2, mode, program)

	def rasterize_flat_triangle(self, v0, v1, v2, mode, program):
		if int(v0.screenCoord.y) == int(v1.screenCoord.y) and int(v1.screenCoord.y) == int(v2.screenCoord.y):
			left = v0 if v0.screenCoord.x < v1.screenCoord.x else v1
			left = left if left.screenCoord.x < v2.screenCoord.x else v2
			right = v0 if v0.screenCoord.x > v1.screenCoord.x else v1
			right = right if right.screenCoord.x > v2.screenCoord.x else v2
			self.draw_scanline(left, right, int(v0.screenCoord.y), mode, program)
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
				self.draw_scanline(left, right, yStart, mode, program)
				return
			for y in xrange(yStart, yEnd + 1, 1):
				interpolateLeft = self.interpolate_rasterize_data(left, bottom, float(y - yStart) / (yEnd - yStart))
				interpolateRight = self.interpolate_rasterize_data(right, bottom, float(y - yStart) / (yEnd - yStart))
				self.draw_scanline(interpolateLeft, interpolateRight, y, mode, program)
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
				self.draw_scanline(left, right, yStart, mode, program)
				return
			for y in xrange(yStart, yEnd + 1, 1):
				interpolateLeft = self.interpolate_rasterize_data(top, left, float(y - yStart) / (yEnd - yStart))
				interpolateRight = self.interpolate_rasterize_data(top, right, float(y - yStart) / (yEnd - yStart))
				self.draw_scanline(interpolateLeft, interpolateRight, y, mode, program)
		else:
			raise Exception('rasterize_flat_triangle should only handle flat triangle!', v0.screenCoord, v1.screenCoord, v2.screenCoord)

	def draw_scanline(self, left, right, y, mode, program):
		xStart = int(left.screenCoord.x)
		xEnd = int(right.screenCoord.x + 1)
		currentFragment = left
		for x in xrange(xStart, xEnd, 1):
			if 0 <= x < self.width and 0 <= y < self.height:
				depthInBuffer = self.graphicsPipeline.get_depth(x, y)
				if currentFragment.screenCoord.z < depthInBuffer:
					self.graphicsPipeline.set_depth(x, y, currentFragment.screenCoord.z)
					color = self.graphicsPipeline.fragmentProcessor.process(currentFragment, program)
					r = int(255 * color.x) % 256
					g = int(255 * color.y) % 256
					b = int(255 * color.z) % 256
					self.rasterize_point(x, y, (r, g, b))
			currentFragment = self.interpolate_rasterize_data(left, right, float(x + 1 - xStart) / (xEnd - xStart))

	def interpolate_rasterize_data(self, v0, v1, t):
		rasterData = RasterizeData()
		rasterData.interpolateParam = srmath.lerp(v0.interpolateParam, v1.interpolateParam, t)
		rasterData.screenCoord = srmath.lerp(v0.screenCoord, v1.screenCoord, t)
		for varyingName in v0.fragmentAttrs.iterkeys():
			rasterData.fragmentAttrs[varyingName] = srmath.lerp(v0.fragmentAttrs[varyingName], v1.fragmentAttrs[varyingName], t)
		return rasterData

	def get_flat_triangles(self, v0, v1, v2):
		triList = [v0, v1, v2]
		triList.sort(key = lambda x : x.screenCoord.y)
		if int(triList[0].screenCoord.y) == int(triList[1].screenCoord.y) or \
			int(triList[1].screenCoord.y) == int(triList[2].screenCoord.y):
			return ((triList[0], triList[1], triList[2]), )
		else:
			t = (triList[1].screenCoord.y - triList[0].screenCoord.y) / (triList[2].screenCoord.y - triList[0].screenCoord.y)
			v3 = self.interpolate_rasterize_data(triList[0], triList[2], t)
			#make sure v3's y is equal to triList[1] to eleminate potential float accurate issue
			v3.screenCoord.y = triList[1].screenCoord.y
			return ((triList[0], triList[1], v3, ), (v3, triList[1], triList[2], ), )

	def rasterize_triangle_wireframe(self, v0, v1, v2, color):
		self.rasterize_line(int(v0.screenCoord.x), int(v0.screenCoord.y), int(v1.screenCoord.x), int(v1.screenCoord.y), color)
		self.rasterize_line(int(v1.screenCoord.x), int(v1.screenCoord.y), int(v2.screenCoord.x), int(v2.screenCoord.y), color)
		self.rasterize_line(int(v2.screenCoord.x), int(v2.screenCoord.y), int(v0.screenCoord.x), int(v0.screenCoord.y), color)

	def rasterize_line(self, x0, y0, x1, y1, color):
		if x0 == x1 and y0 == y1:
			#single point
			self.rasterize_point(x0, y0, color)
		elif x0 == x1:
			#vertical line
			step = 1 if y1 > y0 else -1
			for y in xrange(y0, y1, step):
				self.rasterize_point(x0, y, color)
			self.rasterize_point(x1, y1, color)
		elif y0 == y1:
			#horizontal line
			step = 1 if x1 > x0 else -1
			for x in xrange(x0, x1, step):
				self.rasterize_point(x, y0, color)
			self.rasterize_point(x1, y1, color)
		else:
			delta_x = x0 - x1 if x0 > x1 else x1 - x0
			delta_y = y0 - y1 if y0 > y1 else y1 - y0
			error_term = 0
			if delta_x > delta_y:
				step = 1 if x1 > x0 else -1
				y = y0
				for x in xrange(x0, x1, step):
					self.rasterize_point(x, y, color)
					error_term += delta_y
					if error_term >= delta_x:
						error_term -= delta_x
						y += 1 if y1 > y0 else -1
						self.rasterize_point(x, y, color)
				self.rasterize_point(x1, y1, color)
			else:
				step = 1 if y1 > y0 else -1
				x = x0
				for y in xrange(y0, y1, step):
					self.rasterize_point(x, y, color)
					error_term += delta_x
					if error_term >= delta_y:
						error_term -= delta_y
						x += 1 if x1 > x0 else -1
						self.rasterize_point(x, y, color)
				self.rasterize_point(x1, y1, color)

	def rasterize_point(self, x, y, color):
		self.graphicsPipeline.set_pixel(x, y, color)
	
	def cull_back_face(self, rasterDatas):
		dir0 = rasterDatas[1].screenCoord - rasterDatas[0].screenCoord
		dir1 = rasterDatas[2].screenCoord - rasterDatas[1].screenCoord
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
	
	def check_cvv_out(self, rasterInput):
		outType = 0
		outType |= 0x01 if rasterInput.clipPos.x > rasterInput.clipPos.w else 0
		outType |= 0x02 if rasterInput.clipPos.x < -rasterInput.clipPos.w else 0
		outType |= 0x04 if rasterInput.clipPos.y > rasterInput.clipPos.w else 0
		outType |= 0x08 if rasterInput.clipPos.y < -rasterInput.clipPos.w else 0
		outType |= 0x10 if rasterInput.clipPos.z > rasterInput.clipPos.w else 0
		outType |= 0x20 if rasterInput.clipPos.z < -rasterInput.clipPos.w else 0

		return outType

	def cull_cvv(self, cvvOutTypes):
		if cvvOutTypes[0] & cvvOutTypes[1] & cvvOutTypes[2]:
			return True
		return False


	def process(self, rasterInputs, mode, wireframeColor, program):
		outTypes = [self.check_cvv_out(rasterInput) for rasterInput in rasterInputs]
		if self.cull_cvv(outTypes):
			return
		rasterDatas = [self.init_raster_data(rasterInput) for rasterInput in rasterInputs]
		if self.cull_back_face(rasterDatas):
			return
		self.rasterize_triangle(rasterDatas, mode, wireframeColor, program)
