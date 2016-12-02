# -*- coding: utf-8 -*-
from window import Window
import OpenGL.GLUT as GLUT
import OpenGL.GL as GL
from OpenGL.GL import shaders
import ctypes
import numpy
import scene
import time
import srmath

class OpenGLWindow(Window):
	def __init__(self, graphicsPipeline):
		super(OpenGLWindow, self).__init__(graphicsPipeline)
		self.vao = None
		self.program = None
		self.displayTex = None
		self.renderScene = scene.Scene(graphicsPipeline)
		self.frameCount = 0
		self.lastFrameTime = 0.0


	def getGLError(self):
		return GL.glGetError()

	def init_opengl_texture(self, pixelData):
		textureData = pixelData
		width, height = self.graphicsPipeline.get_frame_buffer_dimension()
		if not self.displayTex:
			self.displayTex = GL.glGenTextures(1)
			GL.glBindTexture(GL.GL_TEXTURE_2D, self.displayTex)
			GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
			GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
		GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGB, width, height, 0, GL.GL_RGB, GL.GL_UNSIGNED_BYTE, textureData)

	def on_window_resize(self, width, height):
		width, height = self.graphicsPipeline.get_frame_buffer_dimension()
		GLUT.glutReshapeWindow(width, height)

	def update_screen(self):
		self.graphicsPipeline.clear_screen()
		self.graphicsPipeline.clear_depth_buffer()
		self.renderScene.update()
		self.graphicsPipeline.swap_front_back_buffers()
		self.init_opengl_texture(self.graphicsPipeline.get_frame_buffer_data())
		GL.glClear(GL.GL_COLOR_BUFFER_BIT)
		GL.glUseProgram(self.program)
		GL.glBindVertexArray(self.vao)
		GL.glDrawArrays(GL.GL_QUADS, 0, 4)
		GL.glBindVertexArray(0)
		GL.glUseProgram(0)
		GL.glFlush()
		GLUT.glutSwapBuffers()


	def window_update(self):
		self.update_statistic_info()
		self.update_screen()
		GLUT.glutPostRedisplay()

	def move_camera(self, direction):
		if direction == 'left':
			offset = srmath.vec3(-0.5, 0.0, 0.0)
		elif direction == 'right':
			offset = srmath.vec3(0.5, 0.0, 0.0)
		elif direction == 'up':
			offset = srmath.vec3(0.0, 0.5, 0.0)
		elif direction == 'down':
			offset = srmath.vec3(0.0, -0.5, 0.0)
		self.renderScene.move_camera(offset)
		# self.graphicsPipeline.clear_screen()
		# self.graphicsPipeline.clear_depth_buffer()

	def on_key_down(self, key):
		direction = ''
		if isinstance(key, str):
			if key.lower() == 'a':
				direction = 'left'
			elif key.lower() == 's':
				direction = 'down'
			elif key.lower() == 'd':
				direction = 'right'
			elif key.lower() == 'w':
				direction = 'up'
			if ord(key) == 27:
				GLUT.glutDestroyWindow(self.window)
				self.window = None
		elif isinstance(key, int):
			if key == GLUT.GLUT_KEY_LEFT:
				direction = 'left'
			if key == GLUT.GLUT_KEY_RIGHT:
				direction = 'right'
			if key == GLUT.GLUT_KEY_UP:
				direction = 'up'
			if key == GLUT.GLUT_KEY_DOWN:
				direction = 'down'
		if direction != '':
			self.move_camera(direction)
				
	def on_mouse_wheel_scroll(self, delta):
		self.renderScene.cam.fov -= delta / 100
		# self.graphicsPipeline.clear_screen()
		# self.graphicsPipeline.clear_depth_buffer()

	def init_gl(self):
		clearColor = self.graphicsPipeline.clearColor
		GL.glClearColor(clearColor[0] / 255.0, clearColor[1] / 255.0, clearColor[2] / 255.0, 1.0)
		GL.glDisable(GL.GL_DEPTH_TEST)
		#init shader program
		with open('opengl_default.vs', 'r') as vsFile:
			vsSource = vsFile.read()
		with open('opengl_default.ps', 'r') as psFile:
			psSource = psFile.read()
		vertexShader = shaders.compileShader(vsSource,GL.GL_VERTEX_SHADER)
		fragmentShader = shaders.compileShader(psSource, GL.GL_FRAGMENT_SHADER)
		self.program = shaders.compileProgram(vertexShader, fragmentShader)

		#init vao and vbos
		vertices = numpy.array([-1.0, -1.0, 0.1, 1.0, 1.0, -1.0, 0.1, 1.0, 1.0, 1.0, 0.1, 1.0, -1.0, 1.0, 0.1, 1.0], dtype=numpy.float32)
		texcoords = numpy.array([0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0], dtype=numpy.float32)

		self.vao = GL.glGenVertexArrays(1)
		GL.glBindVertexArray(self.vao)

		vbo0 = GL.glGenBuffers(1)
		GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vbo0)
		position = GL.glGetAttribLocation(self.program, 'position')
		GL.glEnableVertexAttribArray(position)
		GL.glVertexAttribPointer(position, 4, GL.GL_FLOAT, False, 0, ctypes.c_void_p(0))
		GL.glBufferData(GL.GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL.GL_STATIC_DRAW)

		vbo1 = GL.glGenBuffers(1)
		GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vbo1)
		texcoord = GL.glGetAttribLocation(self.program, 'texcoord')
		GL.glEnableVertexAttribArray(texcoord)
		GL.glVertexAttribPointer(texcoord, 2, GL.GL_FLOAT, False, 0, ctypes.c_void_p(0))
		GL.glBufferData(GL.GL_ARRAY_BUFFER, texcoords.nbytes, texcoords, GL.GL_STATIC_DRAW)


		GL.glBindVertexArray(0)
		GL.glDisableVertexAttribArray(0)
		GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)

	def update_statistic_info(self):
		now = time.time()
		self.frameCount += 1
		deltaFrameTime = now - self.lastFrameTime
		GLUT.glutSetWindowTitle("FPS %.1f/s frameTime:%.2fs" % (1.0 / deltaFrameTime, deltaFrameTime))
		self.lastFrameTime = now

	def on_mouse_event(self, button, state, x, y):
		if button not in (3, 4):
			return
		delta = 50 if state == GLUT.GLUT_UP else -50
		self.on_mouse_wheel_scroll(delta)

		
	def init(self):
		GLUT.glutInit()
		width, height = self.graphicsPipeline.get_frame_buffer_dimension()
		GLUT.glutInitDisplayMode(GLUT.GLUT_RGBA)
		GLUT.glutInitWindowSize(width, height)
		self.window = GLUT.glutCreateWindow('GL')
		GLUT.glutDisplayFunc(self.window_update)
		GLUT.glutReshapeFunc(self.on_window_resize)
		GLUT.glutKeyboardFunc(lambda key, x, y : self.on_key_down(key))
		GLUT.glutSpecialFunc(lambda key, x, y : self.on_key_down(key))
		GLUT.glutMouseFunc(self.on_mouse_event)
		clearColor = self.graphicsPipeline.clearColor
		GL.glClearColor(clearColor[0] / 255.0, clearColor[1] / 255.0, clearColor[2] / 255.0, 1)
		self.init_gl()

		GLUT.glutMainLoop()
