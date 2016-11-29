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
		self.program = shadermgr.get_shader_mgr().create_program()
		self.program.vs = shadermgr.get_shader_mgr().create_shader('VertexColorVS')
		self.program.fs = shadermgr.get_shader_mgr().create_shader('VertexColorFS')
		self.texChessboard = texturemgr.get_tex_mgr().create_chess_board_texture(400, 400, \
				srmath.vec3(20.0 / 255, 160.0 /255, 135.0 /255), srmath.vec3(160.0 /255, 204.0 /255, 20.0 /255))
		self.program.fs.set_uniform('texChessboard', self.texChessboard)

	def move_camera(self, offset, st = space.SpaceType.VIEW_SPACE):
		self.cam.move(offset, st)

	def update(self):
		import cProfile
		pr = cProfile.Profile()
		pr.enable()
		self.draw_cube()
		# self.draw_plane()
		pr.disable()
		outfile = r'f:\PySoftRenderer\profresult'
		s = open(outfile, 'wb')
		sortby = 'cumulative'
		import pstats
		ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
		ps.dump_stats(outfile + '.prof')
		ps.print_stats()
		s.close()

	def draw_cube(self):
		c = simplemesh.Cube(2)
		transformMat = srmath.make_translation_mat(srmath.vec3(0, 1, 0))
		self.graphicsPipeline.draw_mesh(c, self.cam, self.program, transformMat, color.WHITE, pipeline.DrawMode.FILL)

	def draw_plane(self):
		p = simplemesh.Plane(3, 3)
		self.graphicsPipeline.draw_mesh(p, self.cam, self.program, srmath.mat4.identity, color.WHITE, pipeline.DrawMode.FILL)


