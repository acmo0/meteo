#!/usr/bin/python3
def readfile(filename):
	data=None
	try:
		with open(filename, "r") as f:
			data = f.read()
	except:
		pass
	return data
def beetwin(mini, value, maxi):
	if value >= mini and value<=maxi:
		return True
	return False

def bissextile(year):
	if year%4==0:
		if year%100!=0:
			return True
		elif year%400 ==0:
			return True
		else:
			return False
	else:
		return False
#retrun nb of days in a month
def days(month, year):
	#define some values to convert
	nb_month = {1:"janvier", 2:"février", 3:"mars", 4:"avril", 5:"mai", 6:"juin", 7:"juillet", 8:"août", 9:"septembre", 10:"octobre", 11:"novembre", 12:"décembre"}
	nb31 = ["janvier", "mars", "mai", "juillet", "août", "octobre", "décembre"]
	nb30 = ["avril", "juin", "septembre", "novembre"]
	#get month name
	month = nb_month[month]
	
	if month == "février":
		if bissextile(year):
			return 29
		else:
			return 28
	elif month in nb30:
		return 30
	else:
		return 31
def nb_sol_neige_mois(month):
	nb = 0
	for day in month:
		if day['neige_sol'] == 1:
			nb +=1
	return nb
def jour_max_mois(month, critere):
	date = {"date":0, "hauteur":0}
	for day in month:
		if day[critere] > date["hauteur"]:
			date["date"] = day["day"]
			date['hauteur'] = day[critere]
	return date
def jours_max_year(year, critere):
	date = {"date":"", "hauteur":0}
	dates = []
	for month in year:
		d = jour_max_mois(month, critere)
		
		if len(str(d['date'])) == 1:
			d['date'] = "0"+str(d['date'])
		if len(str(month[0]['month'])) == 1:
			month[0]['month'] = "0"+str(month[0]['month'])
		if date['hauteur'] < d['hauteur']:
			date['date'] = d['date']+"/"+month[0]['month']
			date['hauteur'] = d['hauteur']
		dates.append({'date':int(d['date']), "hauteur":d['hauteur']})
	return dates, date
def nb_sol_neige(year):
	nb = 0
	nb_mois = []
	for month in year:
		n = nb_sol_neige_mois(month)
		nb += n
		nb_mois.append(n)
	return nb_mois, n
def somme_prec_mois(month):
	if type(month) != list:
		raise TypeError("Must be list not "+str(type(month)))
	prec = 0
	for day in month:
		prec += day["hauteur"]
	return round(prec, 1)
def somme_prec(year):
	somme = 0
	sommes = []
	for month in year:
		somme_mois = somme_prec_mois(month)
		somme += somme_mois
		sommes.append(somme_mois)
	return sommes ,round(somme, 1)
def prec_mois(month):
	if type(month) != list:
		raise TypeError("Must be list not "+str(type(month)))
	prec = []
	for day in months:
		prec.append(day["hauteur"])
	return prec
def moyenne_t_jour(jour):
	return 	round((jour["minimum"]+jour["maximum"])/2, 1)
def moyenne_t_mois(mois):
	if type(mois) != list:
		raise TypeError("Must be list not "+str(type(mois)))
	moyenne = []
	for day in mois:
		moyenne.append(moyenne_t_jour(day))
	return moyenne
def moy(liste):
	return round(sum(liste)/len(liste), 1)
def moyenne_t_an(an):
	moy_an = []
	for mois in an:
		moy_an.append(moy(moyenne_t_mois(mois)))
	return moy_an, moy(moy_an)
def somme_prec_an(an):
	prec = []
	for mois in an:
		prec.append(somme_prec_mois(mois))
	return prec
def all_min_month(month):
	minis = []
	for day in month:
		minis.append(day['minimum'])
	return minis
def all_max_month(month):
	maxis = []
	for day in month:
		maxis.append(day['maximum'])
	return maxis
def nb_jours_gelee_month(month):
	nb = 0
	for day in month:
		if day['minimum'] <= 0 or day['temp_mini_sol'] <= 0:
			nb+=1
	return nb
def nb_jours_gelee(year):
	nb_mois = []
	nb = 0
	for month in year:
		n = nb_jours_gelee_month(month)
		nb_mois.append(n)
		nb += n
	return nb_mois,nb
def jours_t_month(month, mini,maxi):
	nb = 0
	for day in month:
		if  beetwin(mini, day['maximum'], maxi):
			nb +=1
	return nb
def jours_t_year(year, mini, maxi):
	nb = 0
	nb_mois = []
	for month in year:
		n = jours_t_month(month, mini, maxi)
		nb +=n
		nb_mois.append(n)
	return nb_mois, nb
def nb_jours_sans_degel_month(month):
	nb = 0
	for day in month:
		if day['maximum'] <=0:
			nb+=1
	return nb
def nb_jours_sans_degel(year):
	nb_mois = []
	nb = 0
	for month in year:
		n = nb_jours_sans_degel_month(month)
		nb += n
		nb_mois.append(n)
	return nb_mois, nb
def moy_min(year):
	moyenne = 0
	moyennes = []
	for month in year:
		moyennes.append(moy(all_min_month(month)))
	moyenne = moy(moyennes)
	return moyennes, moyenne
def moy_max(year):
	moyenne = 0
	moyennes = []
	for month in year:
		moyennes.append(moy(all_max_month(month)))
	moyenne = moy(moyennes)
	return moyennes, moyenne
def max_month(month):
	maxima = {"date":0, "temperature":-100}
	for day in month:
		if maxima['temperature']<day['maximum']:
			maxima['temperature']=round(day['maximum'],1)
			maxima['date'] = day['day']
	return maxima
def min_month(month):
	minima = {"date":0, "temperature":100}
	for day in month:
		if minima['temperature']>day['minimum']:
			minima['temperature']=round(day['minimum'],1)
			minima['date'] = day['day']
	return minima
def max_year(year):
	maximas = []
	maxima = {"date":"", "temperature":-100}
	for month in year:
		maxmonth = max_month(month)
		maximas.append(maxmonth)
		if maxima['temperature'] < maxmonth['temperature']:
			maxima['temperature'] = maxmonth['temperature']
			if len(str(maxmonth["date"])) == 1:
				maxdate = "0"+str(maxmonth['date'])
			else:
				maxdate = str(maxmonth['date'])
			if len(str(month[0]["month"])) == 1:
				maximonth = "0"+str(month[0]["month"])
			else:
				maximonth=str(month[0]["month"])
			maxima["date"] = maxdate+"/"+maximonth
	return maximas,maxima
def min_year(year):
	minimas = []
	minima = {"date":"", "temperature":100}
	for month in year:
		minmonth = min_month(month)
		minimas.append(minmonth)
		if minima['temperature'] > minmonth['temperature']:
			minima['temperature'] = minmonth['temperature']
			if len(str(minmonth["date"])) == 1:
				mindate = "0"+str(minmonth['date'])
			else:
				mindate = str(minmonth['date'])
			if len(str(month[0]["month"])) == 1:
				minimonth = "0"+str(month[0]["month"])
			else:
				minimonth=str(month[0]["month"])
			minima["date"] = mindate+"/"+minimonth
	return minimas,minima
def nb_days_per_month(month, crit):
	nb = 0
	for day in month:
		if day['nature'] == crit:
			nb +=1
	return nb
def nb_days_year(year, crit):

	nb = 0
	nb_month = []
	for month in year:
		if len(month)>0:
			nb_day_month = nb_days_per_month(month, crit)
			nb_month.append(nb_day_month)
			nb += nb_day_month
	return nb_month, nb