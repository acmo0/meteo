#!/usr/bin/python3

###import Gtk###
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject
import unicodedata, re
###import custom classes###
from bdd_meteo import  MDb
from utilitaries import *
#from warning_save import WarnSave
nb_month = {1:"janvier", 2:"février", 3:"mars", 4:"avril", 5:"mai", 6:"juin", 7:"juillet", 8:"août", 9:"septembre", 10:"octobre", 11:"novembre", 12:"décembre"}

 
class MonthWindow():
	def on_save_and_exit(self, *args):
		self.save()
		self.exit()
	def on_delete_event(self, object, data=None):
		self.destroy(False)
	def on_quit_activate(self, object, data=None):
		self.destroy()
	def on_save_activate(self, object, data=None):
		self.save()
	def __init__(self,application,year, month ):
		self.layout_path = ""
		with open("/usr/local/lib/meteo/var.cfg", 'r') as f:
			self.layout_path = f.read().split('\n')[2].replace(" ", "")
		print(self.layout_path)
		self.base_name = {"minimum":"mini_", "maximum":"maxi_", "temp_mini_sol":"temph_", "nature":"natureprec_", "hauteur":"hprec_", "neige_sol":"neigesol_", "h_neige_sol":"hneige_", "observation":"observations_"}
		self.line_number = {"aucune":0, "pluie":1, "grele":2, "gresil":3, "verglas":4, "orage":5, "neige":6}
		self.year = year
		self.month = month
		self.application = application
		#connect to data base
		self.bdd = MDb()
		#build window
		self.builder  = Gtk.Builder()
		self.builder.add_from_file(self.layout_path+"month_window.glade")
		self.window = self.builder.get_object("month_window")
		self.year_label = self.builder.get_object("year_name")
		self.month_label = self.builder.get_object("month_name")
		#self.other_window.connect("on_month_window_destroy", self.parent.on_month_window_destroy)xit)
		self.year_label.set_text(str(self.year))
		self.month_label.set_text(nb_month[self.month])
		self.window.set_visible(True)
		self.objects = self.get_all_objects()
		self.builder.connect_signals(self)
		self.init_all_objects()
		if self.bdd.yearExist(self.year) and self.bdd.monthExist(self.month, self.year):
			self.values = self.bdd.getMonth(self.month, self.year)
			self.display_values()
		self.window.connect('delete-event', self.on_delete_event)
		self.window.maximize()

		self.application.add_window(self.window)
		self.window.set_title("Météo")
	def display_values(self):
		for line in self.values:
			day = line["day"]
			for key in line.keys():
				if key not in ["month", "year", "day"]:
					object_to_set = self.objects[day-1][key+"_"+str(day)]
					if key == "nature":
						object_to_set.set_active(self.line_number[line[key]])
					elif key == "neige_sol":
						object_to_set.set_active(bool(line[key]))
					elif key == "observation":
						object_to_set.set_text(line[key])
					else:
						object_to_set.set_value(line[key])

						

	def get_all_objects(self):
		objects = []
		for i in range(1, 32):
			objects.append({"year":self.year, "month":self.month, "day":i})
			for key in self.base_name.keys():
				objects[i-1][key+"_"+str(i)] = self.builder.get_object(self.base_name[key]+str(i))
				if i>days(self.month, self.year):
					self.builder.get_object("label_"+str(i)).set_visible(False)
					objects[i-1][key+"_"+str(i)].set_visible(False)
					del objects[i-1][key+"_"+str(i)]

		return objects

	def init_all_objects(self):
		for line in self.objects:
			for key in line.keys():
				object_to_set = line[key]
				if key not in ["day", "month", "year"]:
					if key.split("_")[0] == "nature":
						object_to_set.set_active(0)
					elif key.split("_")[0]+"_"+key.split("_")[1] == "neige_sol":
						object_to_set.set_active(False)
					elif key.split("_")[0] == "observation":
						object_to_set.set_text("")
					else:
						object_to_set.set_value(0.00)

	def get_all_objects_values(self):
		values = []
		for i in range(len(self.objects)):
			line = self.objects[i]
			
			if len(list(line.keys())) == 11:
				values.append({})
				for key in line.keys():
					if key in ["year", "month", "day"]:
						values[i][key] = line[key]
					else:
						key2 = "_".join(key.split("_")[:-1])
						if key.split("_")[0] == "nature":
							values[i][key2] = re.sub("[\u0300-\u036f]", "",unicodedata.normalize("NFD",str.lower(line[key].get_active_text())))
						elif key.split("_")[0]+"_"+key.split("_")[1] == "neige_sol":
							values[i][key2] = int(line[key].get_active())
						elif key.split("_")[0] == "observation":
							values[i][key2] = line[key].get_text()
						else:
							values[i][key2] = line[key].get_value()
		return values

	def save(self):
		self.values_to_save = self.get_all_objects_values()
		self.bdd.saveMultiple(self.values_to_save)
	def exit(self):
		self.application.remove_window(self.window)
		self.window.destroy()
		#self.other_window.emit("on_month_window_destroy", self.window)

	def destroy(self, visible = True):
		values = self.get_all_objects_values()

		if self.bdd.monthExist(self.month, self.year):
			month_bdd = self.bdd.getMonth(self.month, self.year)
			if month_bdd != values:
				dialog_builder =Gtk.Builder()
				dialog_builder.add_from_file(self.layout_path+"warning_save.glade")
				dialog = dialog_builder.get_object("warning_save")
				class Handler:
					def on_yes_clicked(*args):
						dialog.destroy()
						self.save()
						self.exit()
					def on_no_clicked(*args):
						dialog.destroy()
						self.exit()
					def on_cancel_clicked(*args):
						dialog.destroy()
				dialog.set_title("Attention")
				dialog.set_transient_for(self.window)
				dialog.set_modal(True)
				no = dialog_builder.get_object("no")
				yes = dialog_builder.get_object("yes")
				cancel = dialog_builder.get_object("cancel")
				cancel.set_visible(visible)
				dialog_builder.connect_signals(Handler)
				dialog.show_all()
				#warn = WarnSave(self, self.window, self.application)	
			else:
				self.window.destroy()
		else:
			dialog_builder =Gtk.Builder()
			dialog_builder.add_from_file(self.layout_path+"warning_save.glade")
			dialog = dialog_builder.get_object("warning_save")
			class Handler:
				def on_yes_clicked(*args):
					dialog.destroy()
					self.save()
					self.exit()
				def on_no_clicked(*args):
					dialog.destroy()
					self.exit()
				def on_cancel_clicked(*args):
					dialog.destroy()
			dialog.set_title("Attention")
			dialog.set_transient_for(self.window)
			dialog.set_modal(True)
			no = dialog_builder.get_object("no")
			yes = dialog_builder.get_object("yes")
			cancel = dialog_builder.get_object("cancel")
			dialog_builder.connect_signals(Handler)
			dialog.show_all()
			#warn = WarnSave(self, self.window, self.application)
