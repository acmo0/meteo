#!/usr/bin/python3
from bdd_meteo import MDb
from utilitaries import *
class Calc:
	def __init__(self, year):
		self.bdd = MDb()
		self.year = year
		if not self.bdd.yearExist(self.year):
			return False
		self.year_data = self.bdd.getYear(self.year)

	def getMax(self):
		return max_year(self.year_data)
	def getMin(self):
		return min_year(self.year_data)
	def getNbPluie(self):
		return nb_days_year(self.year_data, 'pluie')
	def getNbGreleGresil(self):
		grele_mois, grele_tot = nb_days_year(self.year_data, 'grele')
		gresil_mois, gresil_tot =nb_days_year(self.year_data, 'gresil')
		tot_mois_2 = []
		tot_2 = gresil_tot+grele_tot
		for i in range(len(grele_mois)):
			tot_mois_2.append(grele_mois[i]+gresil_mois[i])
		return tot_mois_2,tot_2
	def getNbNeige(self):
		return nb_days_year(self.year_data, 'neige')
	def getNbVerglas(self):
		return nb_days_year(self.year_data, 'verglas')
	def getNbOrage(self):
		return nb_days_year(self.year_data, 'orage')
	def getMoyMin(self):
		return moy_min(self.year_data)
	def getMoyMax(self):
		return moy_max(self.year_data)
	def getNbGelee(self):
		return nb_jours_gelee(self.year_data)
	def getNbSansDegel(self):
		return nb_jours_sans_degel(self.year_data)
	def getNbTresChauds(self):
		return jours_t_year(self.year_data, 30, 100)
	def getNbChauds(self):
		return jours_t_year(self.year_data, 25, 29.9)
	def getNbAssezChauds(self):
		return jours_t_year(self.year_data, 20, 24.9)
	def getPrec(self):
		return somme_prec(self.year_data)
	def getNbSolNeige(self):
		return nb_sol_neige(self.year_data)
	def getMaxNeige(self):
		return jours_max_year(self.year_data, 'h_neige_sol')
	def getMaxPrec(self):
		return jours_max_year(self.year_data, 'hauteur')
	def getMoy(self):
		return moyenne_t_an(self.year_data)
class CalcAll:
	def __init__(self):
		self.bdd = MDb()
		self.years = self.bdd.yearAlreadyExist()

	#return list of temperature with year and precip
	def getAllPrec(self):
		prec_all = []
		for year in self.years:
			year_data = self.bdd.getYear(year)
			months_prec, year_prec = somme_prec(year_data)
			prec_all.append([year, year_prec])
		prec_all.sort(key=lambda x:x[1])
		return prec_all
#return list of temperature with year and temps
	def getAllTemp(self):
		temp_all = []
		for year in self.years:
			year_data = self.bdd.getYear(year)
			months_temp, year_temp = moyenne_t_an(year_data)
			temp_all.append([year, year_temp])
		temp_all.sort(key=lambda x:x[1])
		return temp_all