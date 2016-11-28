# -*- coding: utf-8 -*-
from window import Window
import OpenGL.GLUT as GLUT
import OpenGL.GL as GL
from OpenGL.GL import shaders
import ctypes
import numpy

class OpenGLWindow(Window):
	def __init__(self, graphicsPipeline):
		super(OpenGLWindow, self).__init__(graphicsPipeline)
		self.vao = None
		self.program = None
		self.displayTex = None


	def getGLError(self):
		return GL.glGetError()

	def init_opengl_texture(self, pixelData):
		textureData = numpy.array(pixelData, numpy.float)
		width, height = self.graphicsPipeline.get_frame_buffer_dimension()
		self.displayTex = GL.glGenTextures(1)
		GL.glBindTexture(GL.GL_TEXTURE_2D, self.displayTex)
		GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
		GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
		GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGB, width, height, 0, GL.GL_RGB, GL.GL_UNSIGNED_BYTE, textureData)

	def window_update(self):
		GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
		GL.glUseProgram(self.program)
		GL.glBindVertexArray(self.vao)
		GL.glDrawArrays(GL.GL_QUADS, 0, 4)
		GL.glBindVertexArray(0)
		GL.glUseProgram(0)
		GLUT.glutSwapBuffers()

	def init_gl(self):
		clearColor = self.graphicsPipeline.clearColor
		GL.glClearColor(clearColor[0] / 255.0, clearColor[1] / 255.0, clearColor[2] / 255.0, 1.0)
		GL.glEnable(GL.GL_DEPTH_TEST)
		#init shader program
		with open('opengl_default.vs', 'r') as vsFile:
			vsSource = vsFile.read()
		with open('opengl_default.ps', 'r') as psFile:
			psSource = psFile.read()
		vertexShader = shaders.compileShader(vsSource,GL.GL_VERTEX_SHADER)
		fragmentShader = shaders.compileShader(psSource, GL.GL_FRAGMENT_SHADER)
		self.program = shaders.compileProgram(vertexShader, fragmentShader)

		#init vao and vbos
		vertices = numpy.array([-1.0, 1.0, 0.1, 1.0, 1.0, 1.0, 0.1, 1.0, 1.0, -1.0, 0.1, 1.0, -1.0, -1.0, 0.1, 1.0], dtype=numpy.float32)
		texcoords = numpy.array([0.0, 1.0, 0.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0], dtype=numpy.float)

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
		GL.glVertexAttribPointer(texcoord, 4, GL.GL_FLOAT, False, 0, ctypes.c_void_p(0))
		GL.glBufferData(GL.GL_ARRAY_BUFFER, texcoords.nbytes, texcoords, GL.GL_STATIC_DRAW)


		GL.glBindVertexArray(0)
		GL.glDisableVertexAttribArray(0)
		GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)

		
	def init(self):
		GLUT.glutInit()
		width, height = self.graphicsPipeline.get_frame_buffer_dimension()
		GLUT.glutInitDisplayMode(GLUT.GLUT_RGBA)
		GLUT.glutInitWindowSize(width, height)
		self.window = GLUT.glutCreateWindow('GL')
		GLUT.glutDisplayFunc(self.window_update)
		clearColor = self.graphicsPipeline.clearColor
		GL.glClearColor(clearColor[0] / 255.0, clearColor[1] / 255.0, clearColor[2] / 255.0, 1)
		self.init_gl()
		self.pixelData = [(0, 0, 255)] * (width * height)
		self.init_opengl_texture(self.pixelData)

		GLUT.glutMainLoop()
