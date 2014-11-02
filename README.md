# Infoskärmarna - Reborn

# Installation

## Requirements

* [Python2](https://www.python.org/downloads/)
* [pip](http://www.pip-installer.org/)
* [git](http://git-scm.com/) och [git-flow](https://github.com/nvie/gitflow)

## Virtualenv

Virtualenv is not mandatory but highly recommended as it makes it much easier to keep your python projects isolated from each other.

	$ pip install virtualenv

[virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/) is also a handy tool for using virtualenv.

## Repository

Clone the repository:

	git clone <repository url>

Initialize git-flow:

	git flow init -d

## Install Python requirements

To start using virtualenv with this project run:

	$ virtualenv venv

Start using the virtualenv environment with the following command:

	$ source venv/bin/activate

**This command needs to be executed each time you start working on the project to make sure you're using the Python environment specific to this project.**

Now, to install all of the Python libraries required you simply run:

	pip install -r requirements.txt


## Development

To create the database:

	$ python manage.py migrate

To start the development server:

	$ python manage.py runserver

The service is now accessible at [http://localhost:8000].

To create a superuser:

    $ python manage.py createsuperuser

The admin interface is available at `/admin/`.

To load some example pages:

    $ python manage.py loaddata fixtures.json


## Deployment

To deploy the service to a webserver use:

	$ fab deploy <username@webserver>

# Architecture

The service is made up of several django apps as described below:

```
info-reborn			- root of the project
	apps			- apps for displaying the various pages
		dagsen		- display lunch menu
		reittiopas	- display bus schedules
		weather		- display weather
	config 			- project configurations
	manager			- app to manage the info screen pages and users
```



