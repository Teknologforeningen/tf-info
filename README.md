# TF - Info
A webservice to display info-screens around [Teknologföreningen](http://www.teknologforeningen.fi).

# Installation

## Requirements

* [Python2](https://www.python.org/downloads/)
* [pip](http://www.pip-installer.org/)
* [git](http://git-scm.com/)
* ([git-flow](https://github.com/nvie/gitflow))

## Virtualenv

Virtualenv is not mandatory but highly recommended as it makes it much easier to keep your python projects isolated from each other.

	$ pip install virtualenv

[virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/) is also a handy tool for using virtualenv.

Alternative ways of keeping your dev environment isolated are [Docker](https://www.docker.com/) (+ [Fig](http://www.fig.sh/)) and [Vagrant](https://www.vagrantup.com/).

## Repository

Clone the repository:

	git clone <repository url>

Initialize git-flow:

	git checkout master && git flow init -d

(If the above command fails you probably need to manually fetch the remote branch 'master')

The `-d` is for the default options. Git-flow needs to be initialized each time you clone the repository.

## Install Python requirements

To start using virtualenv with this project run:

	$ virtualenv venv

Start using the virtualenv environment with the following command:

	$ source venv/bin/activate

**This command needs to be executed each time you start working on the project to make sure you're using the Python environment specific to this project.**

Now, to install all of the Python libraries required you run:

	pip install -r requirements.txt


## Development

To create the database:

	$ python manage.py migrate

To start the development server:

	$ python manage.py runserver

The service is now accessible at http://localhost:8000.

To create a superuser:

    $ python manage.py createsuperuser

The admin interface is available at `/admin/`.

To load some example pages:

    $ python manage.py loaddata fixtures.json


## Deployment

To deploy the service to a webserver use:

	$ fab deploy

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

# Usage

To edit the pages displayed navigate to the admin UI at `/admin/`.

Once you're logged in you can add, remove or edit the pages.

A page stores the url and descriptions of the page to be displayed as well as information about when the page should be displayed. The different apps in the service expose different url that can be used for pages.

|URL         |Description          |App       |
|------------|---------------------|----------|
|/dagsen/    |Today's lunch menu   |dagsen    |
|/reittiopas/|Bus schedules        |reittiopas|
|/calendar/  |Event calendar       |kalender  |

## Page fields

|Field          |Description                                               |
|---------------|----------------------------------------------------------|
|Url            |The url to display (see table above)                      |
|Duration       |Duration (in seconds) to display the page                 |
|Title          |Title to display in the admin interface                   |
|Description    |Description displayed in the admin interface              |
|Edited by      |The user who last edited the page                         |
|Pause at       |Time and date to pause the page. Clear field to unpause.  |
|Date and Time  |Fields to set the time of day and date to display the page|
|Weekdays       |Weekdays to display the page                              |

