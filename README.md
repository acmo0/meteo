***
## Application
This application is used to create graphics and statistics. 
***
## Installation
### Easy
If you want to install it you can use the .deb file for an easier installation and use apt or dpkg
### Custom installation
However you can download all files and all folders and modify "defaultconfig.cfg" and "var.cfg" :
#### "defaultconfig.cfg"
```
database:<path to db>
backup_dir:~/.local/meteo/backup
years_stats_window_width:400
years_stats_window_heigth:650
```
#### "var.cfg"
change :
```
/usr/local/etc/meteo/config.cfg
/usr/local/etc/meteo/defaultconfig.cfg
/usr/local/lib/meteo/layouts/
/usr/local/lib/meteo/images/
```
in :
```
<path to your config file (will be created automatically)>
<where the "defaultconfig.cfg" file is>
<folder with all layouts>
<folder with all images>
```
