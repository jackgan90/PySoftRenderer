# -*- coding: utf-8 -*-
import math
EPSILON = 0.000001

class Vector2D(object):
	def __init__(self, x = 0.0, y = 0.0):
		self.x = x
		self.y = y

	def toTuple(self):
		return (self.x, self.y)

	def __repr__(self):
		return (self.x, self.y).__repr__()

	def __sub__(self, other):
		return Vector2D(self.x - other.x, self.y - other.y)

	def copyFrom(self, v):
		self.x = v.x
		self.y = v.y

	def normalize(self):
		vectorLength = self.length
		if vectorLength > EPSILON:
			self.x /= vectorLength
			sefl.y /= vectorLength

	@property
	def length(self):
		return math.sqrt(self.x * self.x + self.y * self.y)

	@property
	def normalized(self):
		v = Vector2D()
		v.copyFrom(self)
		v.normalize()
		return v

class Triangle(object):
	def __init__(self):
		self.vertex0 = None
		self.vertex1 = None
		self.vertex2 = None

	def sortVertices(self):
		if not isinstance(self.vertex0, Vector2D):
			return

		if not isinstance(self.vertex1, Vector2D):
			return

		if not isinstance(self.vertex2, Vector2D):
			return

		vertices = [self.vertex0, self.vertex1, self.vertex2]
		vertices.sort(key=lambda v : v.y, reverse=True)
		self.vertex0 = vertices[0]
		self.vertex1 = vertices[1]
		self.vertex2 = vertices[2]

	@property
	def vertices(self):
		return [self.vertex0, self.vertex1, self.vertex2]

	def __repr__(self):
		return [self.vertex0, self.vertex1, self.vertex2].__repr__()


if __name__ == '__main__':
	triangle = Triangle()
	triangle.vertex0 = Vector2D(100.0, 100.0)
	triangle.vertex1 = Vector2D(50.0, 200.0)
	triangle.vertex2 = Vector2D(79.0, 50.0)
	triangle.sortVertices()
	print triangle





