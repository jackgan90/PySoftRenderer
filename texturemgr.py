# -*- coding: utf-8 -*-
from texture import Texture

_instance = None
def get_tex_mgr():
	global _instance
	if _instance is None:
		_instance = TextureMgr()
	return _instance

class TextureMgr(object):
	def __init__(self):
		self.textures = dict()

	def create_chess_board_texture(self, w, h, color0, color1, cells = 5):
		tex = Texture(w, h)
		cellWidth = w / cells
		cellHeight = h / cells
		for x in xrange(w):
			for y in xrange(h):
				tex.data.append(color0 if x / cellWidth % 2 == 0  and y / cellHeight % 2 == 0 else color1)
		self.textures[tex.uniqueId] = tex
		return tex

