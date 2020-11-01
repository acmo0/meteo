#!/usr/bin/python3

###import modules###
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject
###import custom classes###
from new_window_dialog import NewYearWindowDialog
from year_chooser_dialog import YearChooserDialog
from month_window import MonthWindow
from graphics import Graph
from year_stats import YearStats, AllStats
import time
###main window class###
class Main:
	def on_janvier_activate(self, object, data=None):
		mWindow = MonthWindow( self.application, self.year, 1)
	def on_fevrier_activate(self, object, data=None):
		mWindow = MonthWindow( self.application, self.year, 2)
	def on_mars_activate(self, object, data=None):
		mWindow = MonthWindow( self.application, self.year, 3)
	def on_avril_activate(self, object, data=None):
		mWindow = MonthWindow( self.application, self.year, 4)
	def on_mai_activate(self, object, data=None):
		mWindow = MonthWindow( self.application, self.year, 5)
	def on_juin_activate(self, object, data=None):
		mWindow = MonthWindow( self.application, self.year, 6 )
	def on_juillet_activate(self, object, data=None):
		mWindow = MonthWindow( self.application, self.year, 7 )
	def on_aout_activate(self, object, data=None):
		mWindow = MonthWindow( self.application, self.year, 8 )
	def on_septembre_activate(self, object, data=None):
		mWindow = MonthWindow( self.application, self.year, 9 )
	def on_octobre_activate(self, object, data=None):
		mWindow = MonthWindow( self.application, self.year, 10 )
	def on_novembre_activate(self, object, data=None):
		mWindow = MonthWindow( self.application, self.year, 11 )
	def on_decembre_activate(self, object, data=None):
		mWindow = MonthWindow( self.application, self.year, 12 )

	def plot(self):
		Graph().plotYear(self.year)
	def on_precedent_select(self, object, data=None):

		self.logo.set_visible(True)
		self.year_layout.set_visible(False)
		self.menu1.set_visible(True)
		self.menu2.set_visible(False)
		self.builder.connect_signals(self)
	def on_reponse(self,object,response):
		if type(response[0]) == int and len(response) == 2 and type(response[-1]) == Gtk.Dialog:
			response[1].destroy()
			del response[1]
			self.year = response[0]
			self.logo.set_visible(False)
			self.year_layout.set_visible(True)
			self.menu1.set_visible(False)
			self.menu2.set_visible(True)
			self.year_label.set_text(str(self.year))
			self.builder.connect_signals(self)
		elif len(response) == 3 and type(response[-1]) == Gtk.Dialog and response[0] =="plot":
			response[2].destroy()
			del response[2]
			self.year = response[1]
			self.plot()
		elif len(response) == 3 and type(response[-1]) == Gtk.Dialog and response[0] =="bilan":
			response[2].destroy()
			del response[2]
			self.year = response[1]
			ystats = YearStats(self.year, self.application)

	def on_bouton_ouvrir_activate(self, object, data=None):
		newYCDialog = YearChooserDialog(self, self.main_window)
	def on_quitter_activate(self, object, data=None):
		self.main_window.destroy()
	def on_bouton_nouveau_activate(self,object, data=None):
		newYWdialog = NewYearWindowDialog(self, self.main_window)
	def on_t_stats_activate(self, object, data=None):
		AllStats('temp', self.application)
	def on_prec_stats_activate(self, object, data=None):
		AllStats('pluie', self.application)
	def on_main_window_destroy(self,object, data=None):
		self.main_window.destroy()
	def on_plot_year_activate(self, *args):
		ycd = YearChooserDialog(self, self.main_window, "plot")
	def on_year_stats_activate(self, *args):
		ycd = YearChooserDialog(self, self.main_window, "bilan")
	def on_plot_all_activate(self, *args):
		Graph().plotAll()
	def __init__(self, application):
		self.layout_path = ""
		with open("/usr/local/lib/meteo/var.cfg", 'r') as f:
			self.layout_path = f.read().split('\n')[2].replace(" ", "")
		print(self.layout_path)
		self.last = 0
		self.application = application
		self.builder = Gtk.Builder()
		self.builder.add_from_file(self.layout_path+"main.glade")
		self.main_window = self.builder.get_object("main_window")
		self.logo=self.builder.get_object("logo")
		self.img_path = ""
		with open('/usr/local/lib/meteo/var.cfg', 'r') as f:
			self.img_path = f.read().split('\n')[3].replace(" ", "")
		self.logo.set_from_file(self.img_path+"logov2.png")
		self.main_window.set_default_icon_from_file(self.img_path+"main_logo.png")
		self.year_layout = self.builder.get_object("year_layout")
		self.year_label = self.builder.get_object("year_label")
		self.menu1 = self.builder.get_object("menubar1")
		self.menu2 = self.builder.get_object("menubar2")
		self.year_layout.set_visible(True)
		self.builder.connect_signals(self)
		self.year_layout.set_visible(False)

		GObject.signal_new('on_reponse', self.main_window, GObject.SIGNAL_RUN_LAST, GObject.TYPE_PYOBJECT, (GObject.TYPE_PYOBJECT,))
		self.main_window.connect('on_reponse', self.on_reponse)
		#GObject.signal_new('on_month_window_destroy', self.main_window, GObject.SIGNAL_RUN_LAST, GObject.TYPE_PYOBJECT, (GObject.TYPE_PYOBJECT,))
		#self.main_window.connect("on_month_window_destroy", self.on_month_window_destroy)
		self.main_window.set_application(self.application)
		self.main_window.set_title('Météo')
		self.main_window.maximize()
		self.main_window.show()