# -*- coding: utf-8 -*-
import Tkinter
from PIL import Image, ImageTk

class Window(object):
	DEFAULT_HEIGHT = 1024
	DEFAULT_WIDTH = 1024
	def __init__(self):
		self.tkWin = None
		self.canvas = None
		self.image = None
		self._height = self.DEFAULT_HEIGHT
		self._width = self.DEFAULT_WIDTH 
		self.frameBuffer = None

	@property
	def height(self):
		return self._height

	@property
	def width(self):
		return self._width

	@height.setter
	def height(self, value):
		self._height = value

	@width.setter
	def width(self, value):
		self._width = value

	def createResources(self):
		if not self.tkWin:
			self.tkWin = Tkinter.Tk()
		if not self.canvas:
			self.canvas = Tkinter.Canvas(self.tkWin, width=self.width, height=self.height)
			self.canvas.pack()
		if not self.image:
			self.image = Image.new('RGB', (self.width, self.height))
	

	def show(self, frameBuffer):
		self.frameBuffer = frameBuffer
		self.createResources()
		self.image.putdata(self.frameBuffer.buffer)
		img = ImageTk.PhotoImage(self.image)
		self.canvas.create_image(self.width / 2, self.height / 2, image=img)
		
		self.tkWin.mainloop()


