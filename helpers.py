# -*- coding: utf-8 -*-

_current_id = 0

def get_unique_id():
	global _current_id
	_current_id += 1
	return _current_id
	
