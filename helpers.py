# -*- coding: utf-8 -*-

cur_id = 0
def genid():
	global cur_id
	cur_id += 1
	return cur_id
