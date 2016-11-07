# -*- coding: utf-8 -*-
#mathematics library
import math

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

	def dot(self, v):
		return self.x * v.x + self.y * v.y

	@property
	def sqrLength(self):
		return self.x * self.x + self.y * self.y

	@property
	def length(self):
		return math.sqrt(self.sqrLength)

	def __repr__(self):
		return (self.x, self.y).__repr__()

	def normalize(self):
		l = self.length
		if l < EPSILON:
			raise Exception('cannot normalize zero-length vector')
		self.x /= l
		self.y /= l
	
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

	def normalize(self):
		l = self.length
		if l < EPSILON:
			raise Exception('cannot normalize zero-length vector')
		self.x /= l
		self.y /= l
		self.z /= l

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

	def __repr__(self):
		return (self.x, self.y, self.z, self.w).__repr__()

	@property
	def sqrLength(self):
		return self.x * self.x + self.y * self.y + self.z * self.z + self.w * self.w

	@property
	def length(self):
		return math.sqrt(self.sqrLength)

	def normalize(self):
		l = self.length
		if l < EPSILON:
			raise Exception('cannot normalize zero-length vector')
		self.x /= l
		self.y /= l
		self.z /= l
		self.w /= l

vec4.zero = vec4(0, 0, 0, 0)

#column-major 3x3 matrix
class mat3(object):
	def __init__(self, matList=None):
		self.elements = [0] * 9
		if matList is None:
			self.elements[0] = self.elements[3] = self.elements[6] = 1
		else:
			for i in xrange(0, 9):
				self.elements[i] = matList[i]

	def __add__(self, m):
		l = []
		for i in xrange(0, 9):
			l.append(self.elements[i] + m.elements[i])
		return mat3(l)
			
	def __sub__(self, m):
		l = []
		for i in xrange(0, 9):
			l.append(self.elements[i] - m.elements[i])
		return mat3(l)

	def __mul__(self, multiplier):
		if not isinstance(multiplier, mat3):
			return mat3(map(lambda x : x * multiplier, self.elements))
		else:
			return None
			
	def transpose(self):
		self.swapElements(1, 3)
		self.swapElements(2, 6)
		self.swapElements(5, 7)
	
	def swapElements(self, idx0, idx1):
		temp = self.elements[idx0]
		self.elements[idx0] = self.elements[idx1]
		self.elements[idx1] = temp

	def __repr__(self):
		res = ''
		for row in xrange(0, 3):
			for column in xrange(0, 3):
				res += repr(self.elements[3 * column + row])
				if column < 2:
					res += ' '
			if row < 2:
				res += '\n'
		return res

mat3.identity = mat3((1,0,0,0,1,0,0,0,1))

