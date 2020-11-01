###import modules###
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

###import custom modules###
from bdd_meteo import  MDb
from utilitaries import *
from warning import Warn
from time import sleep
###used for choosing an already created year###
class YearChooserDialog():

	#used to quit dialog
	def on_cancel_button_clicked(self, object, data=None):
		print("end")
		self.window.destroy()

	#used to validate new year
	def on_validate_button_clicked(self, object, data=None):
		year = self.spin.get_text()
		#if int
		try:
			year = int(year)
		except:
			return

		if beetwin(1970, year, 2030) and self.bdd.yearExist(year):
			self.year = year
			if self.plot == None:
				self.otherwindow.emit("on_reponse", [year, self.window])
				self.window.emit('delete-event', Gdk.Event('delete-event'))
			else:
				self.window.emit('delete-event', Gdk.Event('delete-event'))
				self.otherwindow.emit("on_reponse", [self.plot, year, self.window])
		else:
			warn = Warn("Il semblerait que la valeur entrée ne soie pas bonne ou que l'année n'ait pas encore été crée")
			

	def __init__(self, master, window, plot = None):
		#self of main_window
		self.layout_path = ""
		with open("/usr/local/lib/meteo/var.cfg", 'r') as f:
			self.layout_path = f.read().split('\n')[2].replace(" ", "")
		print(self.layout_path)
		self.master = master
		self.otherwindow = window
		self.plot = plot
		self.builder = Gtk.Builder()
		self.builder.add_from_file(self.layout_path+"choose_window.glade")
		self.window = self.builder.get_object("choose_window")
		self.spin = self.builder.get_object("year_spin")

		#connect signal to get response on the main window
		self.builder.connect_signals(self)
		self.otherwindow.connect("on_reponse",self.master.on_reponse)

		#open db
		self.bdd = MDb()
		self.window.show()