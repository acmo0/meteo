#!/usr/bin/python3

###import modules###
import sqlite3
import os

##import custom classes and modules
from config_rw import MeteoConfig
from utilitaries import *

###define columns names and type###
columns = {"year":"INTEGER","month":"INTEGER", "day":"INTEGER","minimum":"REAL", "maximum":"REAL","nature":"TEXT", "hauteur":"REAL", "neige_sol":"INTEGER", "temp_mini_sol":"REAL","h_neige_sol":"REAL", "observation":"TEXT"}
columns_name = list(columns.keys())
type_translation = {"INTEGER":[str(int), str(bool)], "REAL":[str(float), str(int)], "TEXT":str(str)}

###get configuration###
def getDb():
	mConfig = MeteoConfig()
	config = mConfig.getcfg()
	database_name = config['database']
	return database_name

###test type of value###
def test_value(value, type_value):
	if not str(type(value)) in type_translation[type_value]:
		raise TypeError(value+" must be "+ ' '.join(type_translation[type_value]))

def verify_values(values):
	for line in values:
		for key in line.keys():
			test_value(line[key], columns[key])


###initialize data base###
def initialize_db(db_connection, cursor,column):
	#construct query
	#create table data if not exist
	query = "CREATE TABLE IF NOT EXISTS data ("
	for key in column.keys():
		query+=key+" "+column[key]+", "
	query = query[:-2]
	query+=")"
	#execute query
	cursor.execute(query)
	db_connection.commit()

#MDb class
class MDb:
	def getPath(self):
		return self.database_name
	def __init__(self):
		#connect and initialize
		self.database_name = getDb()
		self.connection = sqlite3.connect(self.database_name)
		self.cursor = self.connection.cursor()
		initialize_db(self.connection, self.cursor, columns)

	#return all years already created
	def yearAlreadyExist(self):
		result = self.cursor.execute("SELECT year FROM data")
		result = result.fetchall()
		years = []
		if result == None:
			return None
		for year in result:
			year = year[0]
			if not year in years:
				years.append(year)
		years.sort()
		return years


	#return if year exist (True or False)
	def yearExist(self, year):
		result = self.cursor.execute("SELECT * FROM data WHERE year=?", (year,)).fetchall()
		if result == []:
			return False
		else:
			return True
	#return if month of a year exist (True or False)
	def monthExist(self, month, year):
		#test if month is an int
		if type(month) != int:
			raise TypeError("month value must be int not "+ str(type(month)))
		#test if month passed in argument is beetwin 1 and 12
		if not beetwin(1, month,12):
			return False
		#execute query to find if month is already created
		if self.yearExist(year):
			result = self.cursor.execute("SELECT * FROM data WHERE year=? and month=?", (year, month,)).fetchall()
			if result == []:
				return False
			else:
				return True
		else:
			return False

	#save data to db
	def save(self,data):
		#test if data is dict
		if type(data) != dict:
			raise TypeError("Must be dict not "+str(type(data)))
		#test if dict size is the right size
		if len(data.keys()) > len(columns.keys()):
			raise ValueError("To many columns passed")
		elif len(data.keys()) < len(columns.keys()):
			raise ValueError("Missing columns :", ', '.join(data.keys()))
		#test if columns name are correct
		if sorted(data.keys()) != sorted(columns.keys()):
			raise ValueError("Wrong column name")
		#construct query
		self.cursor.execute("SELECT * FROM data WHERE year=? AND month=? AND day=?",(data["year"], data["month"], data["day"], ))
		query = "UPDATE OR IGNORE data set "+'=?, '.join(columns_name[3:])+"=? WHERE year="+str(data["year"])+" and month="+str(data["month"])+" and day="+str(data["day"])+";"
		elements = tuple([data[x] for x in columns_name[3:]])
		print(query)
		self.cursor.execute(query, elements)
		values = []
		for key in columns_name:
			d = data[key]
			if type(d)==str:
				d="'"+d+"'"
			else:
				d = str(d)
			values.append(d)
		query = "INSERT OR IGNORE INTO data("+', '.join(columns_name)+") SELECT " +", ".join(values)+" WHERE (Select Changes()=0)"
		print(query)
		self.cursor.execute(query)
		#execute query
		self.connection.commit()

	#used to save a list of dict
	def saveMultiple(self, data):
		if type(data)!= list:
			raise TypeError("Must be list not "+str(type(data)))
		verify_values(data)
		for line in data:
			self.save(line)

	def getMonth(self,month, year):
		#construct query
		query = "SELECT * FROM data WHERE year="+str(year)+" and month="+str(month)
		self.cursor.execute(query)
		values = self.cursor.fetchall()
		columns = self.cursor.execute("SELECT name FROM PRAGMA_TABLE_INFO('data')").fetchall()
		dict_values = []
		for i in range(len(values)):
			dict_values.append({})
			for j in range(len(columns)):
				if type(values[i][j]) == float:
					dict_values[i][columns[j][0]] = round(values[i][j],1)
				else:
					dict_values[i][columns[j][0]] = values[i][j]
		return dict_values
	def getYear(self, year):
		year_data = []
		for i in range(1,13):
			if self.monthExist(i, year):
				year_data.append(self.getMonth(i, year))
		return year_data
	#used to close db
	def close(self):
		print("close")