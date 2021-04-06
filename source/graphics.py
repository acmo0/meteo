#!/usr/bin/python3
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
from bdd_meteo import MDb
from utilitaries import *
from warning import Warn
class Graph:
	def __init__(self):
		self.bdd = MDb()

	def plotYear(self,year):
		if not self.bdd.yearExist(year):
			raise ValueError("Can't plot : month doesn't exist !")
		year_data = self.bdd.getYear(year)

		prec = somme_prec_an(year_data)
		temp = moyenne_t_an(year_data)[0]
		if len(prec) != 12:
			for i in range(len(prec)+1, 13):
				prec.append(0)
		if len(temp) != 12:
			for i in range(len(temp)+1, 13):
				temp.append(0)
		figure, axis1 = plt.subplots()
		loc = plticker.MultipleLocator(base=1.0)
		loc2 = plticker.MultipleLocator(base=50.0)
		axis1.xaxis.set_major_locator(loc)
		plt.tick_params(labelsize=7)
		axis2 = axis1.twinx()
		for i in range(len(temp)):
			print(temp)
			axis2.annotate(str(temp[i]), xy=(i+1-0.1,temp[i]+5), color='r', fontsize=12)
		axis1.set_ylim([-40, 300])
		axis2.set_ylim([-20, 150])
		loc3 = plticker.MultipleLocator(base=5.0)
		axis2.yaxis.set_major_locator(loc3)
		axis1.yaxis.set_major_locator(loc2)
		axis1.bar([1,2,3,4,5,6,7,8,9,10,11,12], prec, color='b')
		axis2.plot([1,2,3,4,5,6,7,8,9,10,11,12], temp, color='r', marker='+')
		axis1.set_xlabel('Année '+str(year))
		axis1.set_ylabel('Précipitations (mm)', color='b')
		axis2.set_ylabel('Température (°C)', color='r')
		figure.set_size_inches(30, 30, forward = True)
		plt.tick_params(labelsize = 7)
		plt.grid()
		plt.show()
	def plotAll(self):

		years = self.bdd.yearAlreadyExist()
		if years == None or years == []:
			warn = Warn("Vous n'avez rentré aucune valeur pour l'instant")
			return
		years_to_plot = []
		years_prec = []
		years_temp = []
		if len(years) == 1:
			print(1)
		else:
			for i in range(years[0], years[-1]+1):
				years_to_plot.append(i)
				if i in years:
					year = self.bdd.getYear(i)
					years_prec.append(sum(somme_prec_an(year)))
					years_temp.append(moy(moyenne_t_an(year)[0]))
				else:
					years_prec.append(0.0)
					years_temp.append(0.0)
		fig, axis1 = plt.subplots()
		plt.xticks(rotation = 90)
		loc = plticker.MultipleLocator(base=1.0)
		loc2 = plticker.MultipleLocator(base=50.0)
		loc3 = plticker.MultipleLocator(base=20.0)
		loc4 = plticker.MultipleLocator(base=5.0)
		axis1.xaxis.set_major_locator(loc)
		axis2 = axis1.twinx()
		for i in range(len(years_to_plot)):
			axis2.annotate(str(years_temp[i]), xy=(years_to_plot[i]-0.2,years_temp[i]+5), color='r', fontsize=6)
		axis1.set_ylim([-40, 1300])
		axis2.set_ylim([-20, 650])
		axis2.yaxis.set_minor_locator(loc4)
		axis2.yaxis.set_major_locator(loc3)
		axis1.yaxis.set_major_locator(loc2)
		axis1.bar(years_to_plot, years_prec)
		axis2.plot(years_to_plot, years_temp, 'r-', marker='o')
		axis1.set_xlabel("Année")
		axis1.set_ylabel("Précipitations (mm)", color='b')
		axis2.set_ylabel('Température (°C)', color='r')
		plt.tick_params(labelsize=7)
		fig.set_size_inches(30, 30, forward = True)
		plt.grid()
		plt.show()
