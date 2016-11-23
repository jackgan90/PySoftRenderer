# -*- coding: utf-8 -*-
import Tkinter
from PIL import Image, ImageTk
import time

WINDOW_HEIGHT = 512
WINDOW_WIDTH = 512
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
FRAME_RATE = 30

frameBuffer = [BLACK] * (WINDOW_HEIGHT * WINDOW_WIDTH)
window = None
canvas = None
image = None
statisticInfo = None
#Statistic info related variables
frameCount = 0
lastFrameTime = 0.0

def destroyWindow(event):
	global canvas
	global window
	global image
	if canvas:
		canvas.destroy()
		canvas = None
	if window:
		window.destroy()
		window = None
	image = None

def fetchDataFromFrameBuffer():
	global image
	if not image:
		image = Image.new('RGB', (WINDOW_WIDTH, WINDOW_HEIGHT))
	image.putdata(frameBuffer)
	img = ImageTk.PhotoImage(image)
	canvas.create_image(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, image=img)
	canvas.image = img

def windowUpdate():
	global frameCount
	global lastFrameTime
	global statisticInfo
	now = time.time()
	frameCount += 1
	deltaFrameTime = now - lastFrameTime
	statisticInfo.set("FPS %.1f/s frameTime:%.2fs" % (1.0 / deltaFrameTime, deltaFrameTime))
	fetchDataFromFrameBuffer()
	lastFrameTime = now
	if window:
		window.after(1000 / FRAME_RATE, windowUpdate)

def main():
	global canvas
	global window
	global image
	global lastFrameTime
	global statisticInfo
	window = Tkinter.Tk()
	window.resizable(0, 0)
	statisticInfo = Tkinter.StringVar()
	statisticLabel = Tkinter.Label(window, textvariable=statisticInfo, fg="red")
	statisticLabel.pack()
	canvas = Tkinter.Canvas(window, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
	canvas.pack()
	fetchDataFromFrameBuffer()
	lastFrameTime = time.time()
	window.after(1000 / FRAME_RATE, windowUpdate)
	window.bind('<Escape>', destroyWindow)
	window.mainloop()


if __name__ == '__main__':
	main()

