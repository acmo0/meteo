#!/usr/bin/python3
import subprocess
import sys
import importlib
def displayError(notified_error, term_error, py_error):
	subprocess.run(["/usr/bin/notify-send", "--icon=error", "Error :"+notified_error])
	subprocess.run(["gnome-terminal","--","/usr/bin/whiptail","--title","Error","--msgbox","Error : "+term_error+":\n"+str(py_error), "8","78"])
def test(packages):
	try:
		import gi
	except Exception as e:
		displayError("can't import gi module", "can't import gi module check if module is installed", e)
		return False
	try:
		gi.require_version("Gtk", "3.0")
		from gi.repository import Gtk
	except Exception as e:
			displayError("can't import correct Gtk version", "can't import correct version of Gtk check if libgtk-3 is installed", e)
			return False
	for package in packages:
		try:
			importlib.import_module(package)
		except Exception as e:
			displayError("can't import "+package+" module", "can't import "+package+" module check if module is installed",e)
			return False
	return True