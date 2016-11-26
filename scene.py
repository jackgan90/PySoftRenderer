# -*- coding: utf-8 -*-
import camera
import srmath
import color
import simplemesh
import pipeline
import space

class Scene(object):
	def __init__(self):
		self.cam = camera.Camera()
		self.cam.position = srmath.vec3(3, 3, 3)
		self.cam.look_at(srmath.vec3(0, 0, 0))

	def move_camera(self, offset, st = space.SpaceType.VIEW_SPACE):
		self.cam.move(offset, st)

	def update(self):
		self.draw_cube()
		self.draw_plane()

	def draw_cube(self):
		c = simplemesh.Cube(2)
		transformMat = srmath.make_translation_mat(srmath.vec3(0, 1, 0))
		pipeline.draw_mesh(c, self.cam, transformMat, color.WHITE, pipeline.DrawMode.VERTEX_COLOR)

	def draw_plane(self):
		p = simplemesh.Plane(3, 3)
		pipeline.draw_mesh(p, self.cam, srmath.mat4.identity, color.WHITE, pipeline.DrawMode.TEXTURE_MAP)


