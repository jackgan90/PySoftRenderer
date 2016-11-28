# -*- coding: utf-8 -*-

class Window(object):
	def __init__(self, graphicsPipeline):
		self.graphicsPipeline = graphicsPipeline
		self.window = None

	def destroy_window(self):
		raise Exception('destroy_window not implemented!', self.__class__.__name__)

	def on_key_down(self, key):
		raise Exception('on_key_down not implemented!', self.__class__.__name__)

	def on_mouse_click(self, x, y):
		raise Exception('on_mouse_click not implemented!', self.__class__.__name__)

	def on_mouse_wheel_scroll(self, delta):
		raise Exception('on_mouse_wheel_scroll not implemented!', self.__class__.__name__)

	def update_screen(self):
		raise Exception('update_screen not implemented!', self.__class__.__name__)

	def window_update(self):
		raise Exception('window_update not implemented!', self.__class__.__name__)

	def update_statistic_info(self):
		raise Exception('update_statistic_info not implemented!', self.__class__.__name__)

	def register_event_listeners(self):
		pass

	def init(self):
		raise Exception('init not implemented!', self.__class__.__name__)
