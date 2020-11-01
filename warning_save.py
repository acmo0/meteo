#!/usr/bin/python3
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject

class WarnSave:
	def on_yes_activate(self, object, data=None):
		self.other_window.emit("on_reponse", True)
		del self.other_window
		self.window.destroy()
		print("emited")
	def on_no_activate(self, object, data=None):
		self.other_window.emit("on_reponse", False)
		del self.other_window
		self.window.destroy()
	def on_quit_event(self, object, data=None):
		return
	def __init__(self, parent, window,application):
		self.layout_path = ""
		with open("/usr/local/lib/meteo/var.cfg", 'r') as f:
			self.layout_path = f.read().split('\n')[2].replace(" ", "")
		print(self.layout_path)

		self.parent = parent
		self.other_window=window
		self.builder = Gtk.Builder()
		self.builder.add_from_file(self.layout_path+"warning_save.glade")
		self.window = self.builder.get_object("warning_save")
		self.yes = self.builder.get_object("yes")
		self.no = self.builder.get_object("no")
		self.builder.connect_signals(self)
		self.window.connect("delete-event", self.on_quit_event)
		self.other_window.connect("on_reponse", self.parent.on_reponse)
		self.window.show()