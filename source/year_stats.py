#!/usr/bin/python3
###import modules###
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject

from utilitaries import *
from stats import *
from config_rw import MeteoConfig
def style(label_str):
	label_str = "<span font='ubuntu regular 13'>"+label_str+'</span>'
	return label_str
class YearStats:
	def grid_classic(self,row, column, values):
		label = Gtk.Label()
		if column == 25:
			label.set_text(style(str(values[1])))
		else:
			if len(values[0]) > column//2:
				label.set_text(style(str(values[0][column//2])))
			else:
				label.set_text(style('?'))
		label.set_use_markup(True)
		self.gridLayout.attach(label, column, row, 1,1)
	def grid_maxi(self, row, column ,values):
		label = Gtk.Label()
		mesure = list(values[0][0].keys())
		mesure.remove('date')
		mesure = mesure[0]
		if column == 25:
			label.set_text(style(str(values[1][mesure])))
		else:
			if len(values[0]) > column //2:
				label.set_text(style(str(values[0][column//2][mesure])))
			else:
				label.set_text(style('?'))
		label.set_use_markup(True)
		self.gridLayout.attach(label, column, row, 1,1)

		label2 = Gtk.Label()
		if column == 25:
			label2.set_text(style(str(values[1]['date'])))
		else:
			if len(values[0]) > column //2:
				label2.set_text(style(str(values[0][column//2]['date'])))
			else:
				label2.set_text(style('?'))
		label2.set_use_markup(True)
		self.gridLayout.attach(label2, column, row+1, 1,1)
	def grid(self,row, column):
		if row == 1:
			self.grid_classic(row, column, self.moyenne)
		if row == 3:
			self.grid_classic(row, column, self.moyenneMini)
		if row == 5:
			self.grid_classic(row, column, self.moyenneMaxi)
		if row == 7:
			self.grid_maxi(row, column, self.maxTemp)
		if row == 10:
			self.grid_maxi(row, column, self.minTemp)
		if row == 13:
			self.grid_classic(row, column, self.nbJoursGelee)
		if row == 15:
			self.grid_classic(row, column, self.nbJoursSansDegel)
		if row == 17:
			self.grid_classic(row, column, self.nbJoursTChauds)
		if row == 19:
			self.grid_classic(row, column, self.nbJoursChauds)
		if row == 21:
			self.grid_classic(row, column, self.nbJoursAssezChauds)
		if row == 23:
			self.grid_classic(row, column, self.totPrecip)
		if row == 25:
			self.grid_classic(row, column, self.nbJoursPluie)
		if row == 27:
			self.grid_classic(row, column, self.nbJoursNeige)
		if row == 29:
			self.grid_classic(row, column, self.nbJoursSolNeige)
		if row == 31:
			self.grid_classic(row, column, self.nbJoursGG)
		if row == 33:
			self.grid_classic(row, column, self.nbJoursOrage)
		if row == 35:
			self.grid_maxi(row, column, self.maxPrec)
		if row == 38:
			self.grid_maxi(row, column, self.maxPrec)
	def __init__(self, year,application):
		self.layout_path = ""
		with open("/usr/local/lib/meteo/var.cfg", 'r') as f:
			self.layout_path = f.read().split('\n')[2].replace(" ", "")
		print(self.layout_path)
		self.application = application
		self.year = year
		self.builder = Gtk.Builder()
		self.builder.add_from_file(self.layout_path+"year_stats.glade")
		self.window = self.builder.get_object("window")
		self.gridLayout = self.builder.get_object("grid")
		self.calc = Calc(self.year)

		self.maxTemp = self.calc.getMax()
		self.minTemp = self.calc.getMin()
		self.maxNeige = self.calc.getMaxNeige()
		self.maxPrec = self.calc.getMaxPrec()

		self.nbJoursPluie = self.calc.getNbPluie()
		self.nbJoursGG = self.calc.getNbGreleGresil()
		self.nbJoursNeige = self.calc.getNbNeige()
		self.nbJoursVerglas = self.calc.getNbVerglas()
		self.nbJoursOrage = self.calc.getNbOrage()
		self.nbJoursSolNeige = self.calc.getNbSolNeige()
		self.nbJoursGelee = self.calc.getNbGelee()
		self.nbJoursSansDegel = self.calc.getNbSansDegel()
		self.nbJoursTChauds = self.calc.getNbTresChauds()
		self.nbJoursChauds = self.calc.getNbChauds()
		self.nbJoursAssezChauds = self.calc.getNbAssezChauds()

		self.moyenneMini = self.calc.getMoyMin()
		self.moyenneMaxi = self.calc.getMoyMax()
		self.moyenne = self.calc.getMoy()

		self.totPrecip = self.calc.getPrec()

		for row in range(1, 41):
			for column in range(1, 26):
				if row in [2,4,6,9,12,14,16,18, 20,22,24,26,28, 30,32,34,37]:
					self.gridLayout.attach(Gtk.Separator(), column, row, 1,1)
				elif column in [2,4,6,8,10,12,14,16, 18,20,22,24]:
					self.gridLayout.attach(Gtk.Separator(), column, row, 1,1)
				else:
					self.grid(row, column)

		self.application.add_window(self.window)
		self.window.maximize()
		self.window.show_all()
class AllStats:
	def __init__(self, critere, application):
		self.layout_path = ""
		with open("/usr/local/lib/meteo/var.cfg", 'r') as f:
			self.layout_path = f.read().split('\n')[2].replace(" ", "")
		print(self.layout_path)
		self.application = application
		self.calc = CalcAll()
		self.builder = Gtk.Builder()
		self.builder.add_from_file(self.layout_path+"class_years.glade")
		self.window = self.builder.get_object("window")
		self.gridLayout = self.builder.get_object("grid")
		self.unit_label = self.builder.get_object('unit')
		self.column = self.builder.get_object("an")
		self.column.set_use_markup(True)
		if critere == 'pluie':
			self.data = self.calc.getAllPrec()
			self.unit_label.set_text(style("Précipitations (mm)"))
		elif critere == 'temp':
			self.data = self.calc.getAllTemp()
			self.unit_label.set_text(style("Température moyenne (°C)"))

		else:
			raise ValueError('Unknow value '+critere+' must be pluie or temp')
		self.unit_label.set_use_markup(True)
		for i in  range(len(self.data)):
			self.gridLayout.insert_row(i)
			label_year = Gtk.Label()
			label_year.set_text( style(str(self.data[i][0])))
			label_year.set_use_markup(True)
			label_value = Gtk.Label()
			label_value.set_text(style(str(self.data[i][1])))
			label_value.set_use_markup(True)
			self.gridLayout.insert_row(i)
			self.gridLayout.attach(label_year,0, i+1, 1,1)
			self.gridLayout.attach(label_value,1, i+1, 1,1)

		conf = MeteoConfig().getcfg()
		self.window.resize(int(conf['years_stats_window_width']), int(conf['years_stats_window_heigth']))
		self.application.add_window(self.window)
		self.window.show_all()