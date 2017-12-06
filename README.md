# limur-api
Limur service backend

# Installation
## Install virtualenv
Install `virtualenv` and `virtualenvwrapper`:
```
sudo pip3 install virtualenv virtualenvwrapper
```

Add following lines to your `.bashrc`:
```sh
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
source /usr/bin/virtualenvwrapper.sh
```

Update envars:
```
source ~/.bashrc
```

## Create virtualenv
```
mkvirtualenv limur
```

Use following commands when start/end working with the venv:
```
workon limur # to start
deactivate # to end
```

TODO: assign project dir to venv

## Install python deps
```
cd <app_root_dir>
pip3 isntall -r requirements.pip
```

## Install postgre db
Install `postgres` from your system repository. Make sure the service is working.

## Initialize postgre cluster
TODO Collation?
```
sudo -u postgres -i
initdb --locale en_US.utf8 -E UTF8 --data-checksums -D '/var/lib/postgres/data'
exit
```

## Create User and DB
```
sudo -u postgres -i
createuser --interactive # name should be 'writer'
createdb --owner=writer --no-password limur-dev
exit
```

## Apply initial migrations
```
cd <app_root_dir>
python manage.py migrate
```

## Run dev server
```
python manage.py runserver 0:9000
```
Now you should be able to open localhost:9000/admin in your browser
