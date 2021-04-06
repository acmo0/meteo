###import modules###
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

###import custom modules
from bdd_meteo import  MDb
from utilitaries import *
from warning import Warn
class NewYearWindowDialog():
	#used to destroy dialog
	def on_cancel_button_clicked(self, object, data=None):
		self.window.destroy()
	#used to test if year is coherent
	def on_validate_button_clicked(self, object, data=None):
		year = self.entry.get_text()
		#if int
		try:
			year = int(year)
		except:
			return

		if beetwin(1970, year, 2030) and not self.bdd.yearExist(year):
			self.year = year
			self.otherwindow.emit("on_reponse", [year, self.window])
			self.window.destroy()
		else:
			warn = Warn("Il semblerait que la valeur entrée ne soie pas bonne\n ou que l'année soit déjà existante")
			

	def __init__(self, master, window):
		self.layout_path = ""
		with open("/usr/local/lib/meteo/var.cfg", 'r') as f:
			self.layout_path = f.read().split('\n')[2].replace(" ", "")
		print(self.layout_path)
		#self of the main_window
		self.master = master
		self.otherwindow = window
		self.builder = Gtk.Builder()
		self.builder.add_from_file(self.layout_path+"new_window.glade")
		self.window = self.builder.get_object("new_window")
		self.entry = self.builder.get_object("year_entry")
		#connect signal to get response on the main window
		self.builder.connect_signals(self)
		self.otherwindow.connect("on_reponse",self.master.on_reponse)
		#open db
		self.bdd = MDb()
		self.window.show()