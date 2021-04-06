***
## Application
This application is used to create graphics and statistics and is developped by Grégoire Frémion.
***
## Installation
### Easy
If you want to install it you can use the .deb file for an easier installation and use apt or dpkg :
```bash
sudo apt install ./meteo.deb
```
### Custom
However you can download all files and all folders and modify "defaultconfig.cfg" and "var.cfg" :
Make sure python3 is installed and install matplotlib for python3 with 
```bash
apt install python3-matplotlib
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
##Todo :
Create a Windows version.
##Contributing
All feedbacks are welcome. For changes please open a issue to discuss about what you would like to change.
##License
[GPLv3.0](https://www.gnu.org/licenses/gpl-3.0.fr.html)
