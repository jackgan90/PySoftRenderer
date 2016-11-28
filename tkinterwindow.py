# -*- coding: utf-8 -*-
from window import Window
import Tkinter
from PIL import Image, ImageTk
import time
import texture
import srmath
import scene

DEFAULT_FRAME_RATE = 30

class TkinterWindow(Window):
	def __init__(self, graphicsPipeline):
		super(TkinterWindow, self).__init__(graphicsPipeline)
		self.frameRate = DEFAULT_FRAME_RATE
		self.window = None
		self.canvas = None
		self.image = None
		self.statisticInfo = None
		self.frameCount = 0
		self.lastFrameTime = 0.0
		self.renderScene = scene.Scene(graphicsPipeline)

	def save_texture(self, tex, filename):
		img = Image.new('RGB', (tex.width, tex.height))
		img.putdata(tex.buffer)
		img.save(filename)

	def save_depth_texture(self):
		textureData = [(int(255 * (x * 0.5 + 0.5)) % 256, 
			int(255 * (x * 0.5 + 0.5)) % 256, int(255 * (x * 0.5 + 0.5)) % 256)\
					for x in self.graphicsPipeline.depthBuffer.data]
		depthTexture = texture.Texture(self.graphicsPipeline.depthBuffer.width, self.graphicsPipeline.depthBuffer.height)
		depthTexture.buffer = textureData
		self.save_texture(depthTexture, 'depth.bmp')

	def destroy_window(self):
		if self.canvas:
			self.canvas.destroy()
			self.canvas = None
		if self.window:
			self.window.destroy()
			self.window = None
		self.image = None

	def on_key_down(self, key):
		if key.lower() in ('a', 'left'):
			self.move_camera('left')
		if key.lower() in ('d', 'right'):
			self.move_camera('right')
		if key.lower() in ('w', 'up'):
			self.move_camera('up')
		if key.lower() in ('s', 'down'):
			self.move_camera('down')

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
		self.graphicsPipeline.clear_screen()
		self.graphicsPipeline.clear_depth_buffer()

	def on_mouse_click(self, x, y):
		color = self.graphicsPipeline.get_pixel(x, y)
		print x, y, color

	def on_mouse_wheel_scroll(self, delta):
		self.renderScene.cam.fov -= delta / 100
		self.graphicsPipeline.clear_screen()
		self.graphicsPipeline.clear_depth_buffer()

	def update_screen(self):
		width, height = self.graphicsPipeline.get_frame_buffer_dimension()
		if not self.image:
			self.image = Image.new('RGB', (width, height))
		self.renderScene.update()
		self.image.putdata(self.graphicsPipeline.get_frame_buffer_data())
		img = ImageTk.PhotoImage(self.image)
		self.canvas.create_image(width / 2, height / 2, image=img)
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

	def register_event_listeners(self):
		self.window.after(1000 / DEFAULT_FRAME_RATE, self.window_update)
		self.window.bind('<Escape>', lambda event: self.destroy_window())
		self.window.bind('<Right>', lambda event: self.on_key_down('right'))
		self.window.bind('<Left>', lambda event: self.on_key_down('left'))
		self.window.bind('<Up>', lambda event: self.on_key_down('up'))
		self.window.bind('<Down>', lambda event: self.on_key_down('down'))
		self.window.bind('<Key>', lambda event: self.on_key_down(event.char))
		self.window.bind('<MouseWheel>', lambda event:self.on_mouse_wheel_scroll(event.delta))
		self.window.bind('<Button-1>', lambda event: self.on_mouse_click(event.x, event.y))
		self.window.bind('<F3>', lambda event : self.save_texture(self.graphicsPipeline.textures[0], 'chessboard.bmp'))
		self.window.bind('<F4>', lambda event : self.save_depth_texture())

	def init(self):
		self.window = Tkinter.Tk()
		self.window.resizable(0, 0)
		self.statisticInfo = Tkinter.StringVar()
		statisticLabel = Tkinter.Label(self.window, textvariable=self.statisticInfo, fg="red")
		statisticLabel.pack()
		width, height = self.graphicsPipeline.get_frame_buffer_dimension()
		self.canvas = Tkinter.Canvas(self.window, width=width, height=height)
		self.canvas.pack()
		self.update_screen()
		self.lastFrameTime = time.time()
		self.register_event_listeners()
		self.window.mainloop()
		
