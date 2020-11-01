#!/usr/bin/python3
import importlib 
import sys
import time
import os
sys.path.append('/usr/local/lib/meteo')
###packages list###
packages = ["sqlite3", 'shutil']


##import custom classes
import import_package_test
from main_window import Main
from config_rw import MeteoConfig
###import modules###
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio, Gdk, GObject
from bdd_meteo import MDb
import gzip
from datetime import datetime

###check if all packages are available###
if not import_package_test.test(packages):
	sys.exit(1)
def save_bdd():
	bdd_path = MDb().getPath()
	backup_dir = MeteoConfig().getcfg()['backup_dir']
	date_time = datetime.now().strftime("%S_%M_%H_%d_%m_%y")
	if backup_dir[-1] != '/':
		backup_dir+='/'
	file_out = backup_dir+'bdd_meteo_'+date_time+".db.gz"
	home_dir =  os.path.expanduser('~')
	try:
		backup_dir = backup_dir.replace('~', home_dir)
		file_out = file_out.replace('~',home_dir)
	except:
		pass
	if not os.path.exists(backup_dir[:-1]):
		os.makedirs(backup_dir[:-1])
	with open(bdd_path, 'rb') as input_file, gzip.open(file_out, 'wb') as output_file:        
		output_file.writelines(input_file)
class MeteoApplication(Gtk.Application):
	def __init__(self):
		Gtk.Application.__init__(self, application_id="com.gregoire.meteo",flags=Gio.ApplicationFlags.FLAGS_NONE)
		self.connect("activate", self.on_activate)
		self.connect("window-removed", self.on_window_removed)
		self.connect("window-added", self.on_window_added)
		self.home_dir = os.path.expanduser("~")
	def on_window_added(self, window, user_data):
		if len(self.get_windows()) == 3:
			user_data.destroy()
			self.get_windows()[1].present()
			self.get_windows()[1].set_focus()


	def on_window_removed(self, window, user_data):
		if type(user_data)==Gtk.ApplicationWindow:
			
			month_window = None
			for window in self.get_windows():
				if type(window) == Gtk.Window:
					month_window = window
			if month_window != None:
				month_window.emit('delete-event', Gdk.Event('delete-event'))
		save_bdd()
	def on_activate(self, data=None):
		main = Main(self)
if __name__ == "__main__":
	app = MeteoApplication()
	app.run(None)