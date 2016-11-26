# -*- coding: utf-8 -*-
import camera
import srmath
import color
import simplemesh
import pipeline
import space
import shadermgr
import texturemgr

class Scene(object):
	def __init__(self, graphicsPipeline):
		self.graphicsPipeline = graphicsPipeline
		self.cam = camera.Camera()
		self.cam.position = srmath.vec3(3, 3, 3)
		self.cam.look_at(srmath.vec3(0, 0, 0))
		self.vs = shadermgr.get_shader_mgr().create_shader('TextureVS')
		self.fs = shadermgr.get_shader_mgr().create_shader('TextureFS')
		self.texChessboard = texturemgr.get_tex_mgr().create_chess_board_texture(400, 400, \
				srmath.vec3(20.0 / 255, 160.0 /255, 135.0 /255), srmath.vec3(160.0 /255, 204.0 /255, 20.0 /255))
		self.fs.set_uniform('texChessboard', self.texChessboard)

	def move_camera(self, offset, st = space.SpaceType.VIEW_SPACE):
		self.cam.move(offset, st)

	def update(self):
		self.draw_cube()
		# self.draw_plane()

	def draw_cube(self):
		c = simplemesh.Cube(2)
		transformMat = srmath.make_translation_mat(srmath.vec3(0, 1, 0))
		self.graphicsPipeline.draw_mesh(c, self.cam, self.vs, self.fs, transformMat, color.WHITE, pipeline.DrawMode.WIRE_FRAME)

	def draw_plane(self):
		p = simplemesh.Plane(3, 3)
		self.graphicsPipeline.draw_mesh(p, self.cam, self.vs, self.fs, srmath.mat4.identity, color.WHITE, pipeline.DrawMode.FILL)


