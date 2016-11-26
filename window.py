# -*- coding: utf-8 -*-
import Tkinter
from PIL import Image, ImageTk
import time
import pipeline
import texture
import srmath
import scene

DEFAULT_FRAME_RATE = 30

class Window(object):
	def __init__(self):
		self.frameRate = DEFAULT_FRAME_RATE
		self.window = None
		self.canvas = None
		self.image = None
		self.statisticInfo = None
		self.frameCount = 0
		self.lastFrameTime = 0.0
		self.renderScene = scene.Scene()

	def save_texture(self, tex, filename):
		img = Image.new('RGB', (tex.width, tex.height))
		img.putdata(tex.buffer)
		img.save(filename)

	def save_depth_texture(self):
		textureData = [(int(255 * (x * 0.5 + 0.5)) % 256, 
			int(255 * (x * 0.5 + 0.5)) % 256, int(255 * (x * 0.5 + 0.5)) % 256) for x in pipeline.depthBuffer.data]
		depthTexture = texture.Texture(pipeline.WINDOW_WIDTH, pipeline.WINDOW_HEIGHT)
		depthTexture.buffer = textureData
		self.save_texture(depthTexture, 'depth.bmp')

	def destroy_window(self, event):
		if self.canvas:
			self.canvas.destroy()
			self.canvas = None
		if self.window:
			self.window.destroy()
			self.window = None
		self.image = None

	def on_key_down(self, event):
		if event.char.lower() == 'a':
			self.move_camera(event, 'left')
		if event.char.lower() == 'd':
			self.move_camera(event, 'right')
		if event.char.lower() == 'w':
			self.move_camera(event, 'up')
		if event.char.lower() == 's':
			self.move_camera(event, 'down')

	def move_camera(self, event, direction):
		if direction == 'left':
			offset = srmath.vec3(-0.5, 0.0, 0.0)
		elif direction == 'right':
			offset = srmath.vec3(0.5, 0.0, 0.0)
		elif direction == 'up':
			offset = srmath.vec3(0.0, 0.5, 0.0)
		elif direction == 'down':
			offset = srmath.vec3(0.0, -0.5, 0.0)
		self.renderScene.move_camera(offset)
		pipeline.clear_screen()
		pipeline.clear_depth_buffer()

	def on_mouse_click(self, event):
		color = pipeline.get_pixel(event.x, event.y)
		print event.x, event.y, color

	def change_fov(self, event):
		self.renderScene.cam.fov -= event.delta / 100
		pipeline.clear_screen()
		pipeline.clear_depth_buffer()

	def update_screen(self):
		if not self.image:
			self.image = Image.new('RGB', (pipeline.WINDOW_WIDTH, pipeline.WINDOW_HEIGHT))
		self.renderScene.update()
		self.image.putdata(pipeline.frameBuffer.data)
		img = ImageTk.PhotoImage(self.image)
		self.canvas.create_image(pipeline.WINDOW_WIDTH / 2, pipeline.WINDOW_HEIGHT / 2, image=img)
		self.canvas.image = img

	def window_update(self):
		self.update_statistic_info()
		self.update_screen()
		if self.window:
			self.window.after(1000 / DEFAULT_FRAME_RATE, self.window_update)

	def update_statistic_info(self):
		now = time.time()
		self.frameCount += 1
		deltaFrameTime = now - self.lastFrameTime
		self.statisticInfo.set("FPS %.1f/s frameTime:%.2fs" % (1.0 / deltaFrameTime, deltaFrameTime))
		self.lastFrameTime = now


	def init(self):
		self.window = Tkinter.Tk()
		self.window.resizable(0, 0)
		self.statisticInfo = Tkinter.StringVar()
		statisticLabel = Tkinter.Label(self.window, textvariable=self.statisticInfo, fg="red")
		statisticLabel.pack()
		self.canvas = Tkinter.Canvas(self.window, width=pipeline.WINDOW_WIDTH, height=pipeline.WINDOW_HEIGHT)

		self.canvas.pack()
		self.update_screen()
		self.lastFrameTime = time.time()
		self.window.after(1000 / DEFAULT_FRAME_RATE, self.window_update)
		self.window.bind('<Escape>', self.destroy_window)
		self.window.bind('<Right>', lambda event: self.move_camera(event, 'right'))
		self.window.bind('<Left>', lambda event: self.move_camera(event, 'left'))
		self.window.bind('<Up>', lambda event: self.move_camera(event, 'up'))
		self.window.bind('<Down>', lambda event: self.move_camera(event, 'down'))
		self.window.bind('<Key>', self.on_key_down)
		self.window.bind('<MouseWheel>', self.change_fov)
		self.window.bind('<Button-1>', self.on_mouse_click)
		self.window.bind('<F3>', lambda event : self.save_texture(pipeline.textures[0], 'chessboard.bmp'))
		self.window.bind('<F4>', lambda event : self.save_depth_texture())
		self.window.mainloop()
		
