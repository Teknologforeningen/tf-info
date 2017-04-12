from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm

env.project_name = 'info-reborn'
env.www_user = 'www-data'
env.project_dir = '/var/www/%s/'%env.project_name
env.sites_available = '/etc/apache2/sites-available/'

def check_uncommitted_changes():
  num_changes_str = local('git status --porcelain | wc -l', capture=True)
  num_changes = int(num_changes_str)
  if num_changes > 0 and not confirm("Uncommited changes, continue anyway?"):
        abort("Aborting at user request.")

def test():
    with settings(warn_only=True):
        result = local('python manage.py test', capture=True)
    if result.failed and not confirm("Tests failed, continue anyway?"):
        abort("Aborting at user request.")

def setup_django(commit, first_install):
  with cd(env.project_dir):
    sudo('tar xvf /tmp/%s.tar'%commit, user=env.www_user)
    sudo('rm /tmp/%s.tar'%commit)

    with prefix('source bin/activate'):
      sudo('pip install -r requirements.txt', user=env.www_user)
      sudo('python manage.py collectstatic --noinput', user=env.www_user)
      sudo('python manage.py migrate', user=env.www_user)
      if first_install:
        sudo('python manage.py loaddata fixtures', user=env.www_user)

  if first_install:
    sudo('a2ensite %s'%env.project_name)

  sudo('apache2ctl configtest')
  sudo('apache2ctl graceful')

def transfer(commit):
  local('git archive %s > %s.tar'%(commit, commit))
  put('%s.tar'%commit, '/tmp/')
  local('rm %s.tar'%commit)

def install():
  puts("This is for first time setup and will import example data, and create web configs.")
  puts("If you want to update an existing installation, run: fab deploy")
  if confirm("Do you really want to perform first time setup?"):
    deploy(None, True)
  else:
    abort("Aborting at user request.")


def deploy(commit=None, first_install=False): # Deploy should not be first install if ran from command line.
  if commit == None:
    commit = local('git rev-parse --abbrev-ref HEAD', capture=True)
    puts('Deploying current branch: %s'%commit)

  check_uncommitted_changes()
  test()
  transfer(commit)
  setup_django(commit, first_install)
