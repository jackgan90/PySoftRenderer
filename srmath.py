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
		if isinstance(multiplier, mat3):
			result = mat3()
			for row in xrange(0, 3):
				for column in xrange(0, 3):
					result.elements[3 * column + row] = 0
					for k in xrange(0, 3):
						result.elements[3 * column + row] += self.elements[3 * k + row] * multiplier.elements[3 * column + k]
			return result
		elif isinstance(multiplier, vec3):
			result = vec3(0, 0, 0)
			for i in xrange(0, 3):
				for j in xrange(0, 3):
					result[i] += self.elements[3 * j + i] * multiplier[j]
			return result
				
		return mat3(map(lambda x : x * multiplier, self.elements))

	def __getitem__(self, xy):
		if isinstance(xy, int):
			return vec3(self.elements[3 * xy], self.elements[3 * xy + 1], self.elements[3 * xy + 2])
		elif isinstance(xy, tuple):
			column, row = xy
			return self.elements[3 * column + row]
		else:
			raise Exception('mat3 __getitem__ only support int or tuple index')

	def __setitem__(self, xy, val):
		if isinstance(xy, int):
			if isinstance(val, collections.Iterable):
				for i in xrange(3):
					self.elements[3 * xy + i] = val[i]
		elif isinstance(xy, tuple):
			column, row = xy
			self.elements[3 * column + row] = val
		else:
			raise Exception('mat3 __setitem__ only support int or tuple index')

			
	def transpose(self):
		self.swapElements(1, 3)
		self.swapElements(2, 6)
		self.swapElements(5, 7)

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

	@property
	def determinant(self):
		result = 0
		result += self.elements[0] * (self.elements[4] * self.elements[8] - self.elements[5] * self.elements[7])
		result += self.elements[3] * (self.elements[2] * self.elements[7] - self.elements[1] * self.elements[8])
		result += self.elements[6] * (self.elements[1] * self.elements[5] - self.elements[2] * self.elements[4])
		return result
	
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
