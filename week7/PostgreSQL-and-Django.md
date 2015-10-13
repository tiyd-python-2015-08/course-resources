## Installing PostgreSQL

1. Install PostgreSQL using `brew` with the following command: `brew install postgres`
1. Set up the PostgreSQL server to run automatically when you start up your computer with the following command: `ln -sfv /usr/local/opt/postgresql/*.plist ~/Library/LaunchAgents`
1. Start the PostgreSQL server immediately with the following command: `launchctl load ~/Library/LaunchAgents/homebrew.mxcl.postgresql.plist`

Note that the default Postgres config file is located at `/usr/local/var/postgres/pg_hba.conf`

If you'd like a GUI for browsing your database, check out [Postico](https://eggerapps.at/postico/).


## Installing pg modules for Django

1. Add the following to your requirements.txt and install with `pip -r requirements.txt`:
```
psycopg2
```
1. Set up a user and database for your app with the following commands (replacing the square brackets with your information):
```bash
createdb [YOUR PROJECT NAME]
createuser -SDR [YOUR PROJECT NAME]
psql -d postgres -c "ALTER USER [YOUR PROJECT NAME] WITH PASSWORD '[YOUR SECRET PASSWORD]';"
psql -d postgres -c "GRANT ALL PRIVILEGES ON DATABASE [YOUR PROJECT NAME] TO [YOUR PROJECT NAME];"
```
1. Update the DATABASES dict in your project's `settings.py` file to look like the following (replacing square brackets):
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '[YOUR PROJECT NAME]',
        'USER': '[YOUR PROJECT NAME]',
        'PASSWORD': '[YOUR SECRET PASSWORD]',
        'HOST': '',
        'PORT': '',
    }
}
```
1. Run `python manage.py migrate` to set up your tables on your new database.

### Wiping the DB
If you need to trash the database, you don't need to repeat all of the above steps. Just run the following commands to delete and recreate your db:
```
dropdb [YOUR PROJECT NAME]
createdb [YOUR PROJECT NAME]
python manage.py migrate
```
