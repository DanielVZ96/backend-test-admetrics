# ConvCLPUSD
> An API that converts between CLP and USD.

ConvCLPUSD is a django service that with a bit of help from webscrapping, mantains and exposes a database of historical
rates data between the chilean peso(CLP) and the US dollar(USD).

It grabs the data every morning at about 9:35 am from the chilean tax administration and updates the database for the 
current date.


## Installation
- Requirements:
Python 3.53, pip and a bunch of python dependencies included in requirements.txt which we'll install now, such as celery, aiohttp, beautifulsoup, and of course, django.

- Create virtualenv (recommended):
```
$ pip install virtualenv
$ virtualenv <target dir>
$ source <target dir>/bin/activate
```

- Install requirements.txt:

```
$ pip install -r requirements.txt
```

- Migrate database:
```
(in proyect root)$ python manage.py migrate
```

- Retrieve data from sii.cl:
```
$ python manage.py updaterates -a 
```

With these instructions you should have a development server ready for running. Deployment options are up to you.
I recommend running the service with gunicorn, supervisord and nginx, but that's your choice. Have fun!

(In case you want to set up celery with another broker, please refer to the celery documentation)

#### Running celery:
For the database to update periodically you'll have to get the celery worker running. It'll do most of the work for you.
You just have to run this in the project root directory:
```
$ celery -A convclpusd worker -B -l info
```
The -A stands for the app directory in which our celery script lives, in this case backend_test. The worker will
be launched with the -B and -l info parameters. The -B one will get celery beat running (the program in charge of running 
the webscapper periodically).

If you want to learn more about running celery in the background, check out their documentation here:
http://docs.celeryproject.org/en/latest/userguide/daemonizing.html

(Credits to celery documentation)


## Usage

##### Run development server and use the API: 
```
$ python manage.py runserver
$ curl -G 'http://127.0.0.1:8000/clp?usd=100&date=20001002
{"date":"2000-10-02T00:00:00","value":56349.0,"exact_date":true}  # returns a json response
$ curl -G 'http://127.0.0.1:8000/usd?clp=10000&date=20050101'
{"date":"2004-12-30","value":18.0,"exact_date":false}
```
The response always returns three values: date, value, exact_date. The first two are self-explanatory, but
exact_date needs a little explanation. Not all dates have the luxury of getting their own exchange rate.
Exchange rates are only published on weekdays and thus, weekends and some festivities get no exchange rate. 

In practice, we only care for the value of our conversion at some given time, but just know that if
for some reason you receive a different date  than the one you requested and exact_date is false, you are getting
the valid value at that moment, which is the last one published.

##### Manually (and programmatically) update the database:
 The service comes with a handy management command that lets you update the rates database:
 ```
 $ python manage.py updaterates
 Successfully updated rates!
 ```
 This command updates just the current date. If you want to get or update all of the historical rates you have to run
 the command with the -a or --all flag:
 ```
 $ python manage.py uodate -a
 Successfully updated all rates!
 ```
 Actually, you can also call this command from within any script as long as you import the server settings accordingly.
 For example:
 ````
 # myscript.py
 import os
 from django.core.management import call_command
 
 os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_test.settings')
 
 call_command('updaterates')
 ````
 
## Reusing the API:
All of the functionality was carefully encapsulated inside the convclpusd app, so if you are in need of adding some 
usd-clp converter in any other django project, just copy the convclpusd folder, add it into your project's 
installed_apps and copy the celery settings at the bottom of backend_test.settings over to yours.


## About

Daniel Valenzuela – dsvalenzuela@uc.cl

Distributed with some random license. See ``LICENSE`` for more information.

[https://github.com/DanielVZ96/backend-test-admetrics](https://github.com/DanielVZ96/backend-test-admetrics)



