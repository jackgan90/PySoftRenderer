
from PIL import Image, ImageTk
import Tkinter
pixels = []
for x in xrange(1024):
	for y in xrange(1024):
		pixels.append((128, 0, 0))

window = Tkinter.Tk()
canvas = Tkinter.Canvas(window, width=1024, height=1024)
canvas.pack()
pilImage = Image.new('RGB', (1024, 1024))
pilImage.putdata(pixels)
image = ImageTk.PhotoImage(pilImage)
imagesprite = canvas.create_image(512, 512, image=image)
window.mainloop()
