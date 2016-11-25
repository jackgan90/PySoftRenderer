# -*- coding: utf-8 -*-
#mathematics library
import math
import collections

EPSILON = 0.00001

class vec2(object):
	def __init__(self, x = 0.0, y = 0.0):
		self.x = x
		self.y = y

	def __add__(self, v):
		return vec2(self.x + v.x, self.y + v.y)

	def __sub__(self, v):
		return vec2(self.x - v.x, self.y - v.y)

	def __mul__(self, scalar):
		v = vec2(self.x, self.y)
		v.x *= scalar
		v.y *= scalar
		return v
	
	def __div__(self, scalar):
		v = vec2(self.x, self.y)
		v.x /= scalar
		v.y /= scalar
		return v

	def __getitem__(self, i):
		if i == 0:
			return self.x
		elif i == 1:
			return self.y
		else:
			raise Exception('vec2 only has 2 components')

	def __setitem__(self, i, val):
		if i == 0:
			self.x = val
		elif i == 1:
			self.y = val
		else:
			raise Exception('vec2 only has 2 components')

	def __iter__(self):
		yield self.x
		yield self.y
		yield self.z

	def dot(self, v):
		return self.x * v.x + self.y * v.y

	@property
	def sqrLength(self):
		return self.x * self.x + self.y * self.y

	@property
	def length(self):
		return math.sqrt(self.sqrLength)

	@property
	def negate(self):
		return vec2(-self.x, -self.y)

	def __repr__(self):
		return (self.x, self.y).__repr__()

	def normalize(self):
		l = self.length
		if l < EPSILON:
			raise Exception('cannot normalize zero-length vector')
		self.x /= l
		self.y /= l
	
	def toList(self):
		return [self.x, self.y]

	def fromList(self, l):
		self.x, self.y = l[0], l[1]
		
		
	
vec2.zero = vec2(0, 0)
	

class vec3(object):
	def __init__(self, x = 0.0, y = 0.0, z = 0.0):
		self.x = x
		self.y = y
		self.z = z

	def __add__(self, v):
		return vec3(self.x + v.x, self.y + v.y, self.z + v.z)

	def __sub__(self, v):
		return vec3(self.x - v.x, self.y - v.y, self.z - v.z)

	def __mul__(self, scalar):
		v = vec3(self.x, self.y, self.z)
		v.x *= scalar
		v.y *= scalar
		v.z *= scalar
		return v

	def __div__(self, scalar):
		v = vec3(self.x, self.y, self.z)
		v.x /= scalar
		v.y /= scalar
		v.z /= scalar
		return v

	def __getitem__(self, i):
		if i == 0:
			return self.x
		elif i == 1:
			return self.y
		elif i == 2:
			return self.z
		else:
			raise Exception('vec3 only has 3 components')

	def __setitem__(self, i, val):
		if i == 0:
			self.x = val
		elif i == 1:
			self.y = val
		elif i == 2:
			self.z = val
		else:
			raise Exception('vec3 only has 3 components')

	def dot(self, v):
		return self.x * v.x + self.y * v.y + self.z * v.z

	def cross(self, v):
		return vec3(self.y * v.z - self.z * v.y, self.z * v.x - self.x * v.z, self.x * v.y - self.y * v.x)

	def __repr__(self):
		return (self.x, self.y, self.z).__repr__()

	@property
	def sqrLength(self):
		return self.x * self.x + self.y * self.y + self.z * self.z

	@property
	def length(self):
		return math.sqrt(self.sqrLength)

	@property
	def negate(self):
		return vec3(-self.x, -self.y, -self.z)

	def normalize(self):
		l = self.length
		if l < EPSILON:
			raise Exception('cannot normalize zero-length vector')
		self.x /= l
		self.y /= l
		self.z /= l

	def toList(self):
		return [self.x, self.y, self.z]

	def fromList(self, l):
		self.x, self.y, self.z = l[0], l[1], l[2]

vec3.zero = vec3(0, 0, 0)


class vec4(object):
	def __init__(self, x = 0.0, y = 0.0, z = 0.0, w = 0.0):
		self.x = x
		self.y = y
		self.z = z
		self.w = w

	def dot(self, v):
		return self.x * v.x + self.y * v.y + self.z * v.z + self.w * v.w

	def __add__(self, v):
		return vec4(self.x + v.x, self.y + v.y, self.z + v.z, self.w + v.w)

	def __sub__(self, v):
		return vec4(self.x - v.x, self.y - v.y, self.z - v.z, self.w - v.w)

	def __mul__(self, scalar):
		v = vec4(self.x, self.y, self.z, self.w)
		v.x *= scalar
		v.y *= scalar
		v.z *= scalar
		v.w *= scalar
		return v

	def __div__(self, scalar):
		v = vec4(self.x, self.y, self.z, self.w)
		v.x /= scalar
		v.y /= scalar
		v.z /= scalar
		v.w /= scalar
		return v

	def __getitem__(self, i):
		if i == 0:
			return self.x
		elif i == 1:
			return self.y
		elif i == 2:
			return self.z
		elif i == 3:
			return self.w
		else:
			raise Exception('vec4 only has 4 components')

	def __setitem__(self, i, val):
		if i == 0:
			self.x = val
		elif i == 1:
			self.y = val
		elif i == 2:
			self.z = val
		elif i == 3:
			self.w = val
		else:
			raise Exception('vec4 only has 4 components')

	def __repr__(self):
		return (self.x, self.y, self.z, self.w).__repr__()

	@property
	def sqrLength(self):
		return self.x * self.x + self.y * self.y + self.z * self.z + self.w * self.w

	@property
	def length(self):
		return math.sqrt(self.sqrLength)

	@property
	def negate(self):
		return vec4(-self.x, -self.y, -self.z, -self.w)

	def normalize(self):
		l = self.length
		if l < EPSILON:
			raise Exception('cannot normalize zero-length vector')
		self.x /= l
		self.y /= l
		self.z /= l
		self.w /= l
	
	def toList(self):
		return [self.x, self.y, self.z, self.w]

	def fromList(self, l):
		self.x, self.y, self.z, self.w = l[0], l[1], l[2], l[3]

vec4.zero = vec4(0, 0, 0, 0)

#column-major 3x3 matrix
class mat3(object):
	def __init__(self, matList=None):
		self.order = 3
		self.doInit(matList)
	
	def doInit(self, matList):
		self.elementCount = self.order * self.order
		if matList is None:
			self.elements = []
			for i in xrange(0, self.order):
				for j in xrange(0, self.order):
					self.elements.append(int(i == j))
		else:
			self.elements = matList[:self.elementCount]	#for optimization, we don't copy list elements,just use it

	def __add__(self, m):
		l = []
		for i in xrange(0, self.elementCount):
			l.append(self.elements[i] + m.elements[i])
		return self.__class__(l)
			
	def __sub__(self, m):
		l = []
		for i in xrange(0, self.elementCount):
			l.append(self.elements[i] - m.elements[i])
		return self.__class__(l)

	def __mul__(self, multiplier):
		if isinstance(multiplier, self.__class__):
			result = self.__class__()
			for row in xrange(0, self.order):
				for column in xrange(0, self.order):
					result.elements[self.order * column + row] = 0
					for k in xrange(0, self.order):
						result.elements[self.order * column + row] += self.elements[self.order * k + row] * multiplier.elements[self.order * column + k]
			return result
		elif isinstance(multiplier, self.multipliableVecType):
			result = multiplier.__class__()
			for i in xrange(0, self.order):
				for j in xrange(0, self.order):
					result[i] += self.elements[self.order * j + i] * multiplier[j]
			return result
				
		return self.__class__(map(lambda x : x * multiplier, self.elements))

	@property
	def multipliableVecType(self):
		return vec3

	def __getitem__(self, xy):
		if isinstance(xy, int):
			v = self.multipliableVecType()
			for i in xrange(0, self.order):
				v[i] = self.elements[self.order * xy + i]
			return v
		elif isinstance(xy, tuple):
			column, row = xy
			return self.elements[self.order * column + row]
		else:
			raise Exception('%s __getitem__ only support int or tuple index' % self.__class__.__name__)

	def __setitem__(self, xy, val):
		if isinstance(xy, int):
			if isinstance(val, collections.Iterable):
				for i in xrange(self.order):
					self.elements[self.order * xy + i] = val[i]
		elif isinstance(xy, tuple):
			column, row = xy
			self.elements[self.order * column + row] = val
		else:
			raise Exception('%s __setitem__ only support int or tuple index' % self.__class__.__name__)

			
	def transpose(self):
		self.swapElements(1, 3)
		self.swapElements(2, 6)
		self.swapElements(5, 7)

	@property
	def adjugateMat(self):
		m = self.__class__()
		for i in xrange(0, self.elementCount):
			column = i / self.order
			row = i % self.order
			operands = []
			for j in xrange(0, self.elementCount):
				if j / self.order == column or j % self.order == row:
					continue
				operands.append(self.elements[j])
			sign = -1 if (row + column) % 2 else 1
			m.elements[self.order * row + column] = sign * (operands[0] * operands[3] \
					- operands[1] * operands[2])

		return m


	@property
	def determinant(self):
		result = 0
		result += self.elements[0] * (self.elements[4] * self.elements[8] - self.elements[5] * self.elements[7])
		result += self.elements[3] * (self.elements[2] * self.elements[7] - self.elements[1] * self.elements[8])
		result += self.elements[6] * (self.elements[1] * self.elements[5] - self.elements[2] * self.elements[4])
		return result

	def getInverseMat(self):
		det = self.determinant
		if det == 0:
			return None
		else:
			result = mat3()
			det = 1.0 / det
			result.elements[0] = det * (self.elements[4] * self.elements[8] - self.elements[7] * self.elements[5])
			result.elements[1] = det * (self.elements[7] * self.elements[2] - self.elements[1] * self.elements[8])
			result.elements[2] = det * (self.elements[1] * self.elements[5] - self.elements[4] * self.elements[2])
			result.elements[3] = det * (self.elements[6] * self.elements[5] - self.elements[3] * self.elements[8])
			result.elements[4] = det * (self.elements[0] * self.elements[8] - self.elements[6] * self.elements[2])
			result.elements[5] = det * (self.elements[3] * self.elements[2] - self.elements[0] * self.elements[5])
			result.elements[6] = det * (self.elements[3] * self.elements[7] - self.elements[6] * self.elements[4])
			result.elements[7] = det * (self.elements[6] * self.elements[1] - self.elements[0] * self.elements[7])
			result.elements[8] = det * (self.elements[0] * self.elements[4] - self.elements[3] * self.elements[1])
			return result

	def swapElements(self, idx0, idx1):
		temp = self.elements[idx0]
		self.elements[idx0] = self.elements[idx1]
		self.elements[idx1] = temp

	def __repr__(self):
		res = ''
		for row in xrange(0, self.order):
			for column in xrange(0, self.order):
				res += repr(self.elements[self.order * column + row])
				if column < self.order - 1:
					res += ' '
			if row < self.order - 1:
				res += '\n'
		return res
	

mat3.identity = mat3((1,0,0,0,1,0,0,0,1))

class mat4(mat3):
	def __init__(self, matList=None):
		self.order = 4
		self.doInit(matList)

	@property
	def multipliableVecType(self):
		return vec4
	
	def transpose(self):
		self.swapElements(1, 4)
		self.swapElements(2, 8)
		self.swapElements(6, 9)
		self.swapElements(3, 12)
		self.swapElements(7, 13)
		self.swapElements(11, 14)

	@property
	def determinant(self):
		result = 0
		columnLists = []
		idx = 0
		for i in xrange(1, self.elementCount, self.order):
			columnLists.append((idx, self.elements[i:i + 3]))
			idx += 1
		for i in xrange(0, self.order):
			sign = -1 if i % 2 else 1
			l = []
			map(lambda c : l.extend(c[1]) if c[0] != i else [], columnLists)
			result += self.elements[self.order * i] * sign * mat3(l).determinant

		return result

	@property
	def adjugateMat(self):
		m = self.__class__()
		for i in xrange(0, self.elementCount):
			column = i / self.order
			row = i % self.order
			operands = []
			sign = -1 if (row + column) % 2 else 1
			for j in xrange(0, self.elementCount):
				if j / self.order == column or j % self.order == row:
					continue
				operands.append(self.elements[j])
			m.elements[self.order * row + column] = sign * mat3(operands).determinant
		return m


	#seems there's no quick way to calculate a general 4x3 matrix's inverse
	def getInverseMat(self):
		det = self.determinant
		if det == 0:
			return None
		else:
			return self.adjugateMat * (1.0 / det)

mat4.identity = mat4((1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1))

def create_vector(componentCount):
	if componentCount == 2:
		return vec2()
	elif componentCount == 3:
		return vec3()
	elif componentCount == 4:
		return vec4()
	else:
		raise Exception('create_vector only support vec2,vec3,vec4!componentCount is %d' % componentCount)

def make_translation_mat(translation):
	m = mat4()
	m.elements[12] = translation.x
	m.elements[13] = translation.y
	m.elements[14] = translation.z
	return m

def make_scale_mat(scale):
	m = mat4()
	m.elements[0] = scale.x
	m.elements[5] = scale.y
	m.elements[10] = scale.z
	return m

def make_rotation_x_mat(xAngle):
	m = mat4()
	angleInRadians = math.radians(xAngle)
	c = math.cos(angleInRadians)
	s = math.sin(angleInRadians)
	m.elements[5] = c
	m.elements[9] = -s
	m.elements[6] = s
	m.elements[10] = c
	return m

def make_rotation_y_mat(yAngle):
	m = mat4()
	angleInRadians = math.radians(yAngle)
	c = math.cos(angleInRadians)
	s = math.sin(angleInRadians)
	m.elements[0] = c
	m.elements[8] = s
	m.elements[2] = -s
	m.elements[10] = c
	return m

def make_rotation_z_mat(zAngle):
	m = mat4()
	angleInRadians = math.radians(zAngle)
	c = math.cos(angleInRadians)
	s = math.sin(angleInRadians)
	m.elements[0] = c
	m.elements[4] = -s
	m.elements[1] = s
	m.elements[5] = c
	return m

def make_rotation_mat(direction, angle):
	direction.normalize()
	theta = math.radians(angle)
	qsin = math.sin(theta * 0.5)
	qcos = math.cos(theta * 0.5)
	w = qcos
	m = mat4()
	x = direction.x * qsin
	y = direction.y * qsin
	z = direction.z * qsin
	m.elements[0] = 1 - 2 * y * y - 2 * z * z
	m.elements[1] = 2 * x * y + 2 * w * z
	m.elements[2] = 2 * x * z - 2 * w * y
	m.elements[4] = 2 * x * y - 2 * w * z
	m.elements[5] = 1 - 2 * x * x - 2 * z * z
	m.elements[6] = 2 * y * z + 2 * w * x
	m.elements[8] = 2 * x * z + 2 * w * y
	m.elements[9] = 2 * y * z - 2 * w * x
	m.elements[10] = 1 - 2 * x * x - 2 * y * y
	return m

#this function provides a faster way to calculate the inverse
#matrix of a 4-order matrix by not calculating the adjugate matrix
#only applies for transformation matrix
def fast_inverse_mat4(m):
	m3elements = []
	for i in xrange(0, 3):
		m3elements.extend(m[i].toList()[:3])
	m3 = mat3(m3elements)
	m3Inverse = m3.getInverseMat()
	if m3Inverse is None:
		return None
	lastColumn = m[3]
	v3 = vec3(-lastColumn.x, -lastColumn.y, -lastColumn.z)
	v3 = m3Inverse * v3
	result = mat4([
		m3Inverse.elements[0], m3Inverse.elements[1], m3Inverse.elements[2], 0,
		m3Inverse.elements[3], m3Inverse.elements[4], m3Inverse.elements[5], 0,
		m3Inverse.elements[6], m3Inverse.elements[7], m3Inverse.elements[8], 0,
		v3.x, v3.y, v3.z, 1,
		])
	return result

#make view matrix by eye position,target position and reference up direction
def make_view_mat(eye, lookat, up):
	zAxis = eye - lookat
	zAxis.normalize()
	xAxis = up.cross(zAxis)
	xAxis.normalize()
	yAxis = zAxis.cross(xAxis)
	return mat4([
		xAxis.x, yAxis.x, zAxis.x, 0,
		xAxis.y, yAxis.y, zAxis.y, 0,
		xAxis.z, yAxis.z, zAxis.z, 0,
		-xAxis.dot(eye), -yAxis.dot(eye), -zAxis.dot(eye), 1.0,
	])

def make_inv_view_mat(eye, lookat, up):
	zAxis = eye - lookat
	zAxis.normalize()
	xAxis = up.cross(zAxis)
	xAxis.normalize()
	yAxis = zAxis.cross(xAxis)
	return mat4([
		xAxis.x, xAxis.y, xAxis.z, 0,
		yAxis.x, yAxis.y, yAxis.z, 0,
		zAxis.x, zAxis.y, zAxis.z, 0,
		eye.x, eye.y, eye.z, 1.0,
	])




def make_perspect_mat(near, far, left, right, top, bottom):
	width = right - left
	height = top - bottom
	depth = far - near
	return mat4([
		2 * near / width, 0, 0, 0,
		0, 2 * near / height, 0, 0,
		(right + left) / width, (top + bottom) / height, -(far + near) / depth, -1,
		0, 0, - 2 * near * far / depth, 0,
	])

#aspectRatio : w/h
#fov:horizontal fov in degrees
def make_perspect_mat_fov(aspectRatio, near, far, fov):
	right = near * math.tan(math.radians(fov / 2.0))
	left = -right
	top = right / aspectRatio
	bottom = -top
	return make_perspect_mat(near, far, left, right, top, bottom)

def ndc_to_screen_coord(ndcPoint, width, height):
	screenPoint = vec3()
	screenPoint.x = (ndcPoint.x * 0.5 + 0.5) * width
	screenPoint.y = (0.5 - ndcPoint.y * 0.5) * height
	screenPoint.z = ndcPoint.z
	return screenPoint

def lerp(val0, val1, t):
	return val0 + (val1 - val0) * t

