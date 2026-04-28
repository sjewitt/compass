# README for imagemap

## Simple setup (not prod!!)

### python http.server

To view the compass, and save stuff to localdata (ATM) just run python3 


```console

$ python3 -m http.server

```
 on default port of :8000. Or - if you really don't want a port on the URL...

```console

$sudo -m http.server 80

```

This will need elevated permissions...
 
### apache2

This may be a bit much. Let's do a Python3 container? running fastAPI/uvicorn, with a sqlite database. 


 
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

 see https://www.typescriptlang.org/docs/
 
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
 
## SASS

https://sass-lang.com/

### deploy

https://sass-lang.com/install
 
i'll use NPM as I have node already installed...

global:

```
$ sudo npm install -g sass
[sudo] password for silas: 

added 17 packages in 3s

2 packages are looking for funding
  run `npm fund` for details
npm notice 
npm notice New minor version of npm available! 9.5.0 -> 9.6.2
npm notice Changelog: https://github.com/npm/cli/releases/tag/v9.6.2
npm notice Run npm install -g npm@9.6.2 to update!
npm notice 

```

# NOTES

> 1 GH account
https://stackoverflow.com/questions/62625513/i-have-2-github-accounts-how-can-i-use-both-when-i-am-working-in-vs-code


 
 - do a http redirect from root path to /static
 - make API endpoints that map to the digits used for the data:
   - save/<user>/

TO UPDATE!!
-----------

 - imagemap generator: https://www.image-map.net/


# Update 05/04/26

## local user

added compose features to allow passing in a local user as per JB.  CLI startup is:

```
uid=$(id -u ${USER}) gid=$(id -g ${USER}) docker compose up
```

And this is handled by the following in compose file:

```
    # pass in user:group from startup arg:
    # - $uid(id -u ${USER}) $gid(id -g ${USER}) docker compose up
    user: ${uid}:${gid}
```

## Container debug

Also in Compose:

```
    ports:
     - "8080:8080"
     - "5678:5678"  <-- HERE
```
Which is read/used by the debugpy in the container Dockerfile...

```
RUN pip install --no-cache-dir debugpy
...
CMD ["python", "-m", "debugpy", "--listen", "0.0.0.0:5678",  "compass.py"]
```
and is managed by a launch.json in VS Code:

```
{
    "version":"0.2.0",
    "configurations":[
        {
            "name":"python: docker debug",
            "type":"python",
            "request":"attach",
            "connect": {
                "host": "localhost",
                "port": 5678
            },
            "pathMappings": [
                {
                    "localRoot": "${workspaceFolder}/",
// This bit is key, it maps the relevant local to container path of the code...
                    "remoteRoot": "/code"
                }
            ]
        }
    ]
}
```

Thanks Chris N

The sector rings need to reflectthe rating applied to teh current compass

# So what needs to happen for the UI is this:

we need getters for 
 - sectors (all, without titles)
 - sector titles (all)
 - quadrants (all, without titles OR sectors)
 - quadrant titles (all)
 - competencis (all)

The actual assembly of a Compass should ONLY be linked in the compass table - therefore ALL of the components should ONLY be discrete objects. What this means is that the definition of the models should be looser, and should only really apply to the assembled Compass complex object.

This ALSO means that the assembly of the compass data should include the TITLES as well - so the individual components are not bound to any given titles at their database table level - which there isn't - so that (I think) means that the model restriction is at fault here??

And then in the edit/create route, I can provide dropdowsn for each sub-component

CREATE SQL:
-----------


insert INTO quadrants (quadrant_summary,quadrant_css_class,quadrant_elem_coords) values ('test','x','y');
insert into rating (title, description) values ('test', 'desr');
insert into quadrant_titles (quadrant_id,title_part, coord_x, coord_y) values (1,1,0,0);
insert into sectors (quadrant_id,summary, description) values (1,'test','test');
insert into sector_titles (sector_id,title_part, coord_x, coord_y) values (1,'sector y',0,0);
insert into compass_definition values (
12,
	'test',
	1,
	1,
	1,
	1,
	1,
	1,
	1,
	1,
	1,
	1,
	1,
	1,
	1,
	1,
	1,
	1,
	1,
	1,
	1,
	1,
	1,
	1,
	1,
	1,
	1,
	1,
	1,
	1,
	1,
	1,
	1,
	1,
	1,
	1,
	1,
	1,
	1,
	1,
	1,
	1,
	1,
	1,
	1,
	1,
	1,
	1,
	1,
	1,
	1,
	1,
	1,
	1,
	1,
	1,
	1,
	1,
	1,
	1,
	1,
	1,
	1,
	1,
	1,
	1,
	1,
	1,
	1,
	1,
	1,
	1
);

# 81 Implements branches:

 - 71_72/sj/remove_component_coords_from_database_and_create_as_globals
 - 74/sj/remove_dependency_on_database_quadrant_css_classname
 - 77/sj/add_home_button_to_other_templates


`.env` usage

https://stackoverflow.com/questions/58602833/flask-app-config-settings-from-env-flaskenv-in-mod-wsgi


## #113: pydantic models to use subclasses to prevent unnecessary ID field in create endpoints

see branch `61/smeg/models_to_not_require_ids_on_create_IN_and_OUT_models`

This is already minimally implemented for `Rating` with `RatingIn` model. (and Competency??)
 - Where create endpoints exist, apply this same model.  This will not alter the underlying functionality, but WILL remove the confusing and unnecessary (in fact, it's ignored) ID fields for create endpoints...
 - Thee are also instances where the models indicate a nested array of sub-objects are needed - they are NOT, they are a legacy of Models with SubModel properties. This also should be addressed in this issue 
 - as part of this, rationalising the API handler module/modules and the router(s) may also occur.

 ### Add endpoints to update

  - `/compass/`		- OK
  - `/compass/quadrant/` (also, nested arrays!) - OK added third model to account
  - `/compass/quadrant/title/`	- OK
  - `/compass/sectors/` (badly named, its adding only one. Also, nested arrays!) - OK
  - `/compass/sectors/titles/` (maybe add a `../title` (singular) as well?)


I thinkj I need to sequentially number the sector description dropdowns - 1 -> 17