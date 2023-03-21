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

Assuming PHP is installed (should be when apache is installed). was quite fiddly, and probably not the best practice... 
And because of the file permissions set above this needs to be done in a certain order...
(note also that it is `mv` not `rename` to - er - rename...)

Assuming no `/compass/` subdirectory, but is a repo of that name:
 
 - first, `cd /var/www` 
 - then, `sudo git clone https://github.com/sjewitt/compass.git` - need sudo because we don't own the `/var/www/` directory
   - this gives us our web contents, and is now serveable at `http://localhost/` if above apache settings are configured
 - but we can't edit yet because we don't own the files. Therefore:
   - `sudo chown silas:silas -R compass` to take ownership of directory and files, recursively.
 - once done, we can point Eclipse at this folder and edit _in-situ_
 
 
## Typescript

 - Install globally (find ref!)
   - first, need `node`: `https://nodejs.dev/en/download/package-manager/`. This gives us `npm` 
   - `sudo npm install -g typescript` (this installs the node version of typescript)
   - `sudo npm install -g ts-node`    (This is a JIT engine for node.js)
   - set up ability to watch for ANY typescript file changes
   - a dependency was a JSON config file IN THE PROJECT ROOT, specifying the files to watch 
     (see https://stackoverflow.com/questions/12799237/how-to-watch-and-compile-all-typescript-sources/66104668#66104668). 
     This was fiddly to find because I went down a rabbit hole looking for a way to run `tsc` through Eclipse. This option is 
     much better:
     
     ```
	{
		"compilerOptions": {},
		"files": ["file1.ts","file2.ts"]
	}
     ```
   - THEN we can open a terminal and simply watch the directory for changes to the specified file(s) 
     `tsc --watch`
       - this is of course dependent on a global install of typescript (via node) 
 
 - add plugin for Eclipse that knows about TS syntax (e.g. LiClipse, WWD)
 - start a file change watcher
 
 
 
 