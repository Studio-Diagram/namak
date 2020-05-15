# Namak
#### Cafe Management System

[![](https://namak.works/static/img/namak_logo.svg)](https://namak.works/)

##### For Installing on Linux do the following steps:
###### If you have mac everything is similar to linux except the places that we mention in the instructions
##### If you have windows you should install python and postgres without commandline // you can follow [This Link](https://medium.com/@9cv9official/creating-a-django-web-application-with-a-postgresql-database-on-windows-c1eea38fe294) for installing postgres
#
## Linux
```
$ sudo apt update
$ sudo apt install python3-pip python3-dev libpq-dev postgresql postgresql-contrib curl
```
## Mac
*** Installing Python and postgres could be done from their websites ***
You could also follow these steps for mac: [This Link](https://flaviocopes.com/postgres-how-to-install/)
```
$ brew install postgresql
$ brew services start postgresql
```
# Linux & Mac
```
$ sudo -u postgres psql
```
# Windows
Open CMD
```
$ psql
```
Now we are in postgres enviroment
##### Windows OS Users can join instruction from here after installing postgres and python
# 
#
```
postgres=# CREATE DATABASE <DATABASE_NAME>;
postgres=# CREATE USER <DATABASE_USERNAME> WITH PASSWORD '<YOUR_DB_PASSWORD>';
postgres=# ALTER ROLE <DATABASE_USERNAME> SET client_encoding TO 'utf8';
postgres=# ALTER ROLE <DATABASE_USERNAME> SET default_transaction_isolation TO 'read committed';
postgres=# ALTER ROLE <DATABASE_USERNAME> SET timezone TO 'UTC';
postgres=# GRANT ALL PRIVILEGES ON DATABASE <DATABASE_NAME> TO <DATABASE_USERNAME>;
postgres=# \q
```
Now we have to make an virtual enviroment for the project
*** In Windows : without sudo -H ***
```
$ sudo -H pip3 install --upgrade pip
$ sudo -H pip3 install virtualenv
$ mkdir ~/namak_workspace
$ cd ~/namak_workspace
$ virtualenv namak_enviroment
$ source namak_enviroment/bin/activate
```
Now your are in namak enviroment
#
```
(namak_enviroment)$ pip install django psycopg2-binary
```
Then we must clone the project in namak workspace:
with SSH mode (for this way you have to add your SSH public key to gitlab):
```
(namak_enviroment)$ git clone git@gitlab.com:diagram.studio/namak/namak.git
```
with HTTP mode:
```
(namak_enviroment)$ git clone https://gitlab.com/diagram.studio/namak/namak.git
```
Installing requirements:
```
(namak_enviroment)$ cd namak
(namak_enviroment)$ pip install -r requirements.txt
```
Adjusting config.py:
```
(namak_enviroment)$ cd accountiboard/accountiboard
(namak_enviroment)$ touch config.py
(namak_enviroment)$ nano config.py
```

Add these lines to config.py file ( **remember to put your own data for values** ):
```
DEBUG = True
DATABASE_NAME = '<DATABASE_NAME>'
DATABASE_USER = '<DATABASE_USERNAME>'
DATABASE_PASSWORD = '<DATABASE_PASSWORD>'
```
Then migrate changes in database:
```
(namak_enviroment)$ cd ..
(namak_enviroment)$ ./manage.py makemigrations
(namak_enviroment)$ ./manage.py migrate
```
### Time to Test:
```
(namak_enviroment)$ ./manage.py runserver 0.0.0.0:8000
```
check this url in your browser
```
http://127.0.0.1:8000
```

#### Creating Superuser

```
(namak_enviroment)$ ./manage.py createsuperuser
```

#### Then Complete the creating with your own data.
#
After that, go to Django Admin Panel with your superuser data and login:
```
http://127.0.0.1:8000/admin/
```
Follow these steps:
* Go to Users and click on ( Add User + )

* Fill First Name and Last name and phone and email with your own data.

* Leaving the Last Login Field blank

* Check the Is active Checkbox

* Fill Password with pbkdf2_sha256$120000$eFM2jCGCoaQg$Wnziyp9xaIrKGkw9Dd3o+mFxFSgp5bMGMFTkdz5u3S0=

* Select cafe_owner option for User Type field

* Fill Birthday Date and Home Address with your own data

* Then Click on save

* Now go to Organization Model

* Click on ( Add Organization + )

* Fill all fields and click on save

* Now go to Cafe Owners Model

* Click on ( Add Cafe Owner + )

* Select your User for User Field

* Select your Organization for Organization Field

* Save the cafe Owner

* Now go to the following Url and login to Namak:
```
Url : http://127.0.0.1:8000
Username: <Your_phone_number_on_User_model>
Password: 1234
```

