***
## Application
This application is used to create graphics and statistics based on your meteorological data and is developped by Grégoire Frémion.
***
## Installation
### Easy
If you want to install it you can use the .deb file located in binary folder for an easier installation and use apt or dpkg :
```bash
sudo apt install ./meteo.deb
```
### Custom
However you can download all files from sources and all folders and modify "defaultconfig.cfg" and "var.cfg" :
Make sure python3 is installed and install matplotlib and for python3 with 
```bash
apt install python3-matplotlib python3-gi python3-gi-cairo gir1.2-gtk-3.0
```
or
```
pip3 install -r requirements.txt 
```
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
<location of the "defaultconfig.cfg" file>
<folder with all layouts>
<folder with all images>
```
***
## Screenshots :
![plot](https://github.com/acmo0/meteo/blob/main/screenshot/screen1.png)
![plot](https://github.com/acmo0/meteo/blob/main/screenshot/edit.png)
![plot](https://github.com/acmo0/meteo/blob/main/screenshot/graph.png)
***
## Todo :
Create a Windows version.
***
## Contributing
All feedbacks are welcome. For changes please open a issue to discuss about what you would like to change.
***
## License
[GPLv3.0](https://www.gnu.org/licenses/gpl-3.0.fr.html)
