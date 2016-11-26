# -*- coding: utf-8 -*-
import buffer3d

class Texture(buffer3d.Buffer3D):
	def __init__(self, w, h):
		super(Texture, self).__init__(w, h)

def create_chess_board_texture(w, h, color0, color1, cells = 5):
	tex = Texture(w, h)
	cellWidth = w / cells
	cellHeight = h / cells
	for x in xrange(w):
		for y in xrange(h):
			tex.data.append(color0 if x / cellWidth % 2 == 0  and y / cellHeight % 2 == 0 else color1)
	return tex
