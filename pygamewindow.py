# -*- coding: utf-8 -*-
from window import Window
import scene
import pygame
import time
import srmath

class PyGameWindow(Window):
	def __init__(self, graphicsPipeline):
		super(PyGameWindow, self).__init__(graphicsPipeline)
		self.clock = pygame.time.Clock()
		self.pixelArray = None
		self.renderScene = scene.Scene(graphicsPipeline)
		self.frameCount = 0
		self.lastFrameTime = 0.0
		self.done = False
		self.eventKeys = [pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_w, 
			pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_ESCAPE]


	def on_key_down(self, key):
		if key in (pygame.K_a, pygame.K_LEFT):
			self.move_camera('left')
		if key in (pygame.K_d, pygame.K_RIGHT):
			self.move_camera('right')
		if key in (pygame.K_w, pygame.K_UP):
			self.move_camera('up')
		if key in (pygame.K_d, pygame.K_DOWN):
			self.move_camera('down')
		if key == pygame.K_ESCAPE:
			self.done = True
			pygame.quit()

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

	def on_mouse_wheel_scroll(self, delta):
		self.renderScene.cam.fov -= delta / 100

	def window_update(self):
		while not self.done:
			# --- Main event loop
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.done = True
				elif event.type == pygame.KEYDOWN:
					if event.key in self.eventKeys:
						self.on_key_down(event.key)
				elif event.type in (pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN):
					if event.button in (4, 5):
						self.on_mouse_wheel_scroll(50 if event.button == 4 else -50)
			if not self.done:
				self.update_statistic_info()
				self.update_screen()
				pygame.display.flip()
				self.clock.tick(self.targetFrameRate)

		pygame.quit()

	def update_statistic_info(self):
		now = time.time()
		self.frameCount += 1
		deltaFrameTime = now - self.lastFrameTime
		pygame.display.set_caption("FPS %.1f/s frameTime:%.2fs" % (1.0 / deltaFrameTime, deltaFrameTime))
		self.lastFrameTime = now

	def update_screen(self):
		self.graphicsPipeline.clear_screen()
		self.graphicsPipeline.clear_depth_buffer()
		self.renderScene.update()
		self.graphicsPipeline.swap_front_back_buffers()
		width, height = self.graphicsPipeline.get_frame_buffer_dimension()
		for x in xrange(width):
			for y in xrange(height):
				self.pixelArray[x, y] = tuple(self.graphicsPipeline.get_pixel(x, y))

	def init(self):
		pygame.init()
		width, height = self.graphicsPipeline.get_frame_buffer_dimension()
		self.window = pygame.display.set_mode((width, height))
		self.pixelArray = pygame.PixelArray(self.window)
		self.window_update()
