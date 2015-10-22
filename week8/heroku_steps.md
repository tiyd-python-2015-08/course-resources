# Heroku

## One-time installation

Run the following commands _just once_ for your system to install the heroku toolbelt.

1. `brew install heroku`
1. `heroku login`

## Deploying an existing project to Heroku

1. Install necessary packages:

  `pip install gunicorn psycopg2 dj-database-url whitenoise`

1. Freeze and replace your requirements:

  `pip freeze>requirements.txt`

1. Create your Heroku instance:

  `heroku create`

1. Set your Heroku environment variables (replace `todomvc` with the folder name of your project):

  ```
  heroku config:set DJANGO_SETTINGS_MODULE=todomvc.heroku_settings
  heroku config:set PYTHONPATH=todomvc
  heroku config:set SECRET_KEY=`python -c 'import random; print("".join([random.choice("abcdefghijklmnopqrstuvwxyz0123456789") for i in range(50)]))'`
  ```

1. Create `heroku_settings.py` in the same folder as your `settings.py`. Example:

  ```python
  from .settings import *
  import os
  import dj_database_url

  DEBUG = bool(int(os.environ.get('DEBUG', False)))
  SECRET_KEY = os.environ['SECRET_KEY']

  BLACKLIST_APPS = ['debugtoolbar', 'django_extensions']

  INSTALLED_APPS = tuple([app for app in INSTALLED_APPS if app not in BLACKLIST_APPS])

  DATABASES['default'] = dj_database_url.config()

  SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

  ALLOWED_HOSTS = ['*']

  # Static asset configuration
  import os
  BASE_DIR = os.path.dirname(os.path.abspath(__file__))
  STATIC_ROOT = 'staticfiles'
  STATIC_URL = '/static/'

  STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
  ```

1. Modify your `settings.py` file to ensure you have a `STATIC_ROOT` setting:

  `STATIC_ROOT = 'staticfiles'`

1. Modify `wsgi.py` to wrap `get_wsgi_application` with `DjangoWhiteNoise` (replace `todomvc` with the folder name of your project):

  ```python
  import os

  from django.core.wsgi import get_wsgi_application
  from whitenoise.django import DjangoWhiteNoise

  os.environ.setdefault("DJANGO_SETTINGS_MODULE", "todomvc.settings")

  application = DjangoWhiteNoise(get_wsgi_application())
  ```

1. Create `Procfile` (replace `todomvc` with the folder name of your project):

  ```
  web: gunicorn todomvc.wsgi --log-file -
  ```

1. Create `runtime.txt`:

  ```
  python-3.4.3
  ```

1. Create a `.env` file for `heroku local` (replace `todomvc` with the folder name of your project):

  ```
  DATABASE_URL=postgres:///todomvc
  DJANGO_SETTINGS_MODULE=todomvc.heroku_settings
  PYTHONPATH=todomvc
  SECRET_KEY=cs5uqcpzq89op51beua4x8yhqh7ep4ows73qkb2y0misd3ncf7
  ```

1. Test your installation locally:

  `heroku local`

1. Stage/commit your code to the master branch, then push that up to heroku:

  ```
  git push heroku
  ```

1. Spin up a dyno:

  `heroku ps:scale web=1`

1. Migrate your database on heroku (replace `todomvc` with the folder name of your project):

  `heroku run python todomvc/manage.py migrate`

1. Open up the app:

  `heroku open`

Check out [this page from Heroku](https://devcenter.heroku.com/articles/getting-started-with-django) for more detailed information.
