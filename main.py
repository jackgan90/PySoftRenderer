# -*- coding: utf-8 -*-
import Tkinter
from PIL import Image, ImageTk
import time
import pipeline
import srmath

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
FRAME_RATE = 30

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

def onKeyDown(event):
	if event.char.lower() == 'a':
		move_camera(event, 'left')
	if event.char.lower() == 'd':
		move_camera(event, 'right')
	if event.char.lower() == 'w':
		move_camera(event, 'up')
	if event.char.lower() == 's':
		move_camera(event, 'down')

def move_camera(event, direction):
	if direction == 'left':
		offset = srmath.vec3(-0.5, 0.0, 0.0)
	elif direction == 'right':
		offset = srmath.vec3(0.5, 0.0, 0.0)
	elif direction == 'up':
		offset = srmath.vec3(0.0, 0.5, 0.0)
	elif direction == 'down':
		offset = srmath.vec3(0.0, -0.5, 0.0)
	pipeline.move_camera(offset)
	pipeline.clear_screen()

def changeFOV(event):
	pipeline.cameraFOV -= event.delta / 100
	pipeline.clear_screen()

def fetchDataFromFrameBuffer():
	global image
	if not image:
		image = Image.new('RGB', (pipeline.WINDOW_WIDTH, pipeline.WINDOW_HEIGHT))
	pipeline.update()
	image.putdata(pipeline.frameBuffer)
	img = ImageTk.PhotoImage(image)
	canvas.create_image(pipeline.WINDOW_WIDTH / 2, pipeline.WINDOW_HEIGHT / 2, image=img)
	canvas.image = img

def windowUpdate():
	updateStatisticInfo()
	fetchDataFromFrameBuffer()
	if window:
		window.after(1000 / FRAME_RATE, windowUpdate)

def updateStatisticInfo():
	global frameCount
	global lastFrameTime
	global statisticInfo
	now = time.time()
	frameCount += 1
	deltaFrameTime = now - lastFrameTime
	statisticInfo.set("FPS %.1f/s frameTime:%.2fs" % (1.0 / deltaFrameTime, deltaFrameTime))
	lastFrameTime = now


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
	canvas = Tkinter.Canvas(window, width=pipeline.WINDOW_WIDTH, height=pipeline.WINDOW_HEIGHT)

	canvas.pack()
	fetchDataFromFrameBuffer()
	lastFrameTime = time.time()
	window.after(1000 / FRAME_RATE, windowUpdate)
	window.bind('<Escape>', destroyWindow)
	window.bind('<Right>', lambda event: move_camera(event, 'right'))
	window.bind('<Left>', lambda event: move_camera(event, 'left'))
	window.bind('<Up>', lambda event: move_camera(event, 'up'))
	window.bind('<Down>', lambda event: move_camera(event, 'down'))
	window.bind('<Key>', onKeyDown)
	window.bind('<MouseWheel>', changeFOV)
	window.mainloop()


if __name__ == '__main__':
	main()

