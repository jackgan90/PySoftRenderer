# -*- coding: utf-8 -*-
import pygame
import geometry
import rasterizer

class DrawContext(object):
	DEFAULT_COLOR = (0, 0, 0)
	def __init__(self, surface):
		self.surface = surface
		self.color = self.DEFAULT_COLOR
		self.flipY = True

	def setColor(self, color):
		self.color = color

	def drawPoint(self, position, color=None):
		if color is None:
			color = self.color
		if self.flipY:
			sur_size = self.surface.get_size()
			position = (position[0], sur_size[1] - position[1])
		pygame.draw.circle(self.surface, color, position, 0)

	def drawLine(self, start, end):
		rasterizer.Bresenham_Integer(start, end, self)


	def drawTriangle(self, triangle, fill=True):
		triangle.sortVertices()
		rasterizer.Bresenham_Triangle(triangle.vertices, self, fill)



	
