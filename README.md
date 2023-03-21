# README for imagemap

## Simple setup (not prod!!)
 
### apache2

 - Install apache2
 - `cd /etc/apache2/sites-available/`
 - `sudo nano 000-default.conf`:
   - update `DocumentRoot` to be `/var/www/compass`
     - we are not doing multiple virtual hosts, so this will serve our Compass on localhost:80 or 127.0.0.1:80
   - apache2 is autostart by default - leave this 
     
### repo and file perms
 - cd to /var/www/
 - do `sudo git clone https://github.com/sjewitt/compass.git`
 - do `sudo chown silas:silas -R compass`
   - leave group/other perms as r or rx (i.e. default) so apache can read them

### watch apache2 logs
 
 - first, `cd var/log/apache2`
 - then, `tail -f access.log` to follow the entries as they are added to teh access log. This is handy when checking requests are going in
 
### PHP dev

Assuming PHP is installed (should be when apache is installed):

 - because of the file permissions set above 