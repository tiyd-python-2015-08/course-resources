# Getting started with Heroku, Django, and PostgreSQL

## Installing PostgreSQL

_(only do these steps **once** on your machine)_

1. Install PostgreSQL using `brew` with the following command: `brew install postgres`
1. Set up the PostgreSQL server to run automatically when you start up your computer with the following command: `ln -sfv /usr/local/opt/postgresql/*.plist ~/Library/LaunchAgents`
1. Start the PostgreSQL server immediately with the following command: `launchctl load ~/Library/LaunchAgents/homebrew.mxcl.postgresql.plist`

Note that the default Postgres config file is located at `/usr/local/var/postgres/pg_hba.conf`

If you'd like a GUI for browsing your database, check out [Postico](https://eggerapps.at/postico/).

## Installing Heroku toolbelt

_(only do these steps **once** on your machine)_

1. `brew install heroku`
1. `heroku login`

## Create your working environment

1. Create your folder and `.envrc` file:

  ```
  mkdir [YOUR PROJECT NAME]
  cd [YOUR PROJECT NAME]
  echo layout python3>.envrc
  ```

1. `direnv allow`
1. `pip install django`

## Clone the starter project

1. `django-admin startproject --template=https://github.com/heroku/heroku-django-template/archive/master.zip --name=Procfile [YOUR PROJECT NAME] .`
1. Update `requirements.txt` to point to the latest versions of available packages:
  ```
  dj-database-url
  Django
  django-postgrespool
  gunicorn
  psycopg2
  SQLAlchemy
  whitenoise
  ```
1. `pip install -r requirements.txt`
1. Refreeze requirements.txt:

  `pip freeze > requirements.txt`

1. `python manage.py startapp [YOUR APP NAME]`
1. Initialize your local git repository:

  `git init .`

## Set local environment variables

You can add various lines to your `.envrc` file to adjust your local environment. Make sure to run `direnv allow` after you've made changes to your `.envrc` file.

1. To use PostgreSQL for local development (recommended):

  `export DATABASE_URL=postgresql:///[YOUR PROJECT NAME]`

1. To enable DEBUG mode on your local machine:

  `export DEBUG=1`

1. Add a SECRET_KEY for local development:
  `export SECRET_KEY=4sfjgpe6wuyq1t8enz1yq8smym3qjbenhz5bijq3p1chqd13w2`

## Setup your Heroku instance

1. Create your Heroku instance:

  `heroku create`

1. Set Heroku environment variables
  ```
  heroku config:set SECRET_KEY=`python -c 'import random; print("".join([random.choice("abcdefghijklmnopqrstuvwxyz0123456789") for i in range(50)]))'`
  heroku config:set DEBUG=1
  ```

## Specify Python 3

1. Edit `runtime.txt` to specify your Python version:

  ```
  python-3.4.3
  ```

## Test Heroku locally

1. `heroku local`

## Deploy to Heroku

1. Add your git files, commit, and push:

  ```
  git add -A
  git commit -m "Initial commit for Heroku"
  git push heroku master
  heroku run python manage.py migrate
  ```

1. Spin up a dyno:

  `heroku ps:scale web=1`

1. Test it out:

  `heroku open`

## Get ready for production

1. Make the following changes to `settings.py` to get production ready:
  ```
  # Replace the existing DEBUG and SECRET_KEY lines with these
  DEBUG = bool(int(os.environ.get('DEBUG', False)))
  SECRET_KEY = os.environ['SECRET_KEY']

  # Put this part AFTER your existing INSTALLED_APPS setting
  if DEBUG:
    BLACKLIST_APPS = ['debugtoolbar', 'django_extensions']

    INSTALLED_APPS = tuple([app for app in INSTALLED_APPS if app not in BLACKLIST_APPS])

  ```
1. Turn debug mode off on heroku:

  `heroku config:set DEBUG=0`

1. Push your changes to heroku:

  `git push heroku master`

Note that this setup does not use a separate `heroku_settings.py` file. You don't need this if you make your dev environment very similar to Heroku and just use environment variables!

Check out [this page from Heroku](https://devcenter.heroku.com/articles/getting-started-with-django) for more detailed information.

### Wiping the DB
If you need to trash the local database, you don't need to repeat all of the above steps. Just run the following commands to delete and recreate your db:

```
dropdb [YOUR PROJECT NAME]
python manage.py migrate
```

To trash the database on heroku, use the Heroku control panel.
