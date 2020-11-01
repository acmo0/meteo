#!/usr/bin/python3
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

#warning popup
class Warn:
	def on_destroy(self,object,data=None):
		self.window.destroy()
	def __init__(self, message):
		self.message = message
		self.layout_path = ""
		with open("/usr/local/lib/meteo/var.cfg", 'r') as f:
			self.layout_path = f.read().split('\n')[2].replace(" ", "")
		print(self.layout_path)
		self.builder = Gtk.Builder()
		self.builder.add_from_file(self.layout_path+"warning.glade")
		self.window = self.builder.get_object("warn")
		self.label = self.builder.get_object("warning_label")
		self.builder.connect_signals(self)
		self.label.set_text(self.message)
		self.window.show()