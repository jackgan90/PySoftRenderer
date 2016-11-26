# -*- coding: utf-8 -*-
import srmath
import space

class Camera(object):
	def __init__(self):
		self.position = srmath.vec3(0, 0, 0)
		self.aspectRatio = 1.0
		self.fov = 60
		self.nearPlane = 1.0
		self.farPlane = 500.0
		self.xAxis = srmath.vec3(1, 0, 0)
		self.yAxis = srmath.vec3(0, 1, 0)
		self.zAxis = srmath.vec3(0, 0, 1)

	def move(self, offset, st = space.SpaceType.VIEW_SPACE):
		if st == space.SpaceType.VIEW_SPACE:
			worldOffset = srmath.vec3()
			worldOffset.x = srmath.vec3(self.xAxis.x, self.yAxis.x, self.zAxis.x).dot(offset)
			worldOffset.y = srmath.vec3(self.xAxis.y, self.yAxis.y, self.zAxis.y).dot(offset)
			worldOffset.z = srmath.vec3(self.xAxis.z, self.yAxis.z, self.zAxis.z).dot(offset)
			self.position += worldOffset
		elif st == space.SpaceType.WORLD_SPACE:
			self.position += offset
		else:
			raise Exception('camera object only support world/view space movement!')

	def look_at(self, at, up = srmath.vec3(0, 1, 0)):
		self.zAxis = self.position - at
		self.zAxis.normalize()
		self.xAxis = up.cross(self.zAxis)
		self.xAxis.normalize()
		self.yAxis = self.zAxis.cross(self.xAxis)

	def get_world_to_view_mat(self):
		return srmath.make_view_mat_axis(self.xAxis, self.yAxis, self.zAxis, self.position)

	def get_projection_mat(self):
		return srmath.make_perspect_mat_fov(self.aspectRatio, self.nearPlane, self.farPlane, self.fov)


